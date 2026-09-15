#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_level.py - Trinh kiem chung du lieu man choi "Linh An Thon - Chapter 1".

CHI DUNG THU VIEN CHUAN CUA PYTHON 3 (json, re, os, sys, argparse, collections).
KHONG import jsonschema / pydantic / requests - moi truong san xuat khong co.

Trinh nay hien thuc hai hop dong:

  1. schema/level.schema.json   -> data/chapter_01.json + data/areas/<area_id>.json
  2. schema/liveops.schema.json -> data/liveops_chapter_01.json

Cac lop kiem tra, theo thu tu chay:

  GIAI DOAN 1  Doc & phan tich JSON
  GIAI DOAN 2  Cau truc: truong bat buoc, kieu du lieu, gia tri enum
  GIAI DOAN 3  Rang buoc co dieu kien theo action_type / trigger_type / puzzle type,
               hotspot USE_ITEM khong sinh hieu ung (no-op)
  GIAI DOAN 4  Hinh hoc: bounds trong 1920x1080, width/height > 0, nguong cham
               120 px @1920 (san cung tuyet doi 88 px), visual_bounds nam tron trong bounds
  GIAI DOAN 5  Hotspot chong lan trong cung mot khu vuc
  GIAI DOAN 6  Dinh danh duy nhat toan chuong + quy uoc tien to
  GIAI DOAN 7  Nguon cap co tien trinh (chi TUONG MINH) + tham chieu cheo
  GIAI DOAN 8  Do thi phu thuoc vat pham: phat hien CHU TRINH (deadlock thiet ke)
  GIAI DOAN 9  Vat pham "chet" + CU DOA CHET (jumpscare khong bao gio ban duoc)
  GIAI DOAN 10 KHA GIAI: mo phong nguoi choi bang thuat toan diem bat dong (fixpoint)
  GIAI DOAN 11 LiveOps: cac bat bien trong data/liveops_chapter_01.json

QUY TAC VANG CUA GIAI DOAN 10 (bai hoc tu mot vong audit):
  Mo phong kha giai CHI duoc nap nhung gi doc duoc TUONG MINH tu du lieu -
  truong grants_flag, required_flags, required_item, required_items, unlock_condition -
  cong dung MOT luat suy dien co dinh: giai cau do X bat co flag_<X>_solved.
  Truoc day trinh kiem con "doan" nguon cap co bang cach so trung tu khoa giua ten co
  va ten hotspot, roi nap chinh cai doan do vao mo phong; ket qua la no in
  "[OK] KHA GIAI ... 5/5 khu vuc" cho mot man choi ma nguoi choi that chi di duoc 2/5.
  Ket luan nguy con nguy hiem hon khong co ket luan. Phan suy luan do gio chi con
  duoc in ra duoi dang [i] GOI Y CHO NGUOI THIET KE va KHONG bao gio vao mo phong.

Ma thoat: 0 = sach (co the con [CANH BAO]), 1 = co it nhat mot [LOI].
Voi --strict thi MOI [CANH BAO] duoc nang thanh [LOI] (dung cho cong CI).

Vi du:
    python3 tools/validate_level.py
    python3 tools/validate_level.py /home/user/HackTheBox/LinhAnThon/data
    python3 tools/validate_level.py --liveops data/liveops_chapter_01.json
    python3 tools/validate_level.py --strict --trace
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict

# --------------------------------------------------------------------------
# HANG SO HOP DONG - dong bo voi schema/level.schema.json
# --------------------------------------------------------------------------

DEFAULT_DATA_DIR = "/home/user/HackTheBox/LinhAnThon/data"

DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080

# NGUONG VUNG CHAM - hai muc, khong phai mot.
#
# Khung thiet ke rong 1920 px duoc thu vua be ngang man hinh dien thoai. Tren cac may
# pho bien (5.5" den 6.7"), 1 px thiet ke rong khoang 0.024 - 0.036 pt vat ly, nen mot
# vung cham 88 px @1920 chi con khoang 29 - 43 pt - THAP HON ca 44 pt cua Apple HIG lan
# 48 dp cua Android Material. Muon dat 44 pt o may nho nhat trong tap muc tieu thi canh
# vung cham phai tu 120 px @1920 tro len.
#
#   canh < HARD_MIN_TOUCH_SIZE (88)  -> [LOI]   khong co ngoai le
#   canh < MIN_TOUCH_SIZE     (120)  -> [CANH BAO], TRU KHI hotspot khai bao visual_bounds
#                                       (tuc la vung cham da duoc no rong co chu dich so
#                                        voi vung ve, va designer da biet viec minh lam)
MIN_TOUCH_SIZE = 120
HARD_MIN_TOUCH_SIZE = 88

ACTION_TYPES = (
    "ZOOM_PUZZLE",
    "COLLECT_ITEM",
    "EXAMINE",
    "USE_ITEM",
    "CHANGE_AREA",
    "DIALOGUE",
)

PUZZLE_TYPES = (
    "ROTATION_LOCK",
    "SEQUENCE_ORDER",
    "SLIDING_TILE",
    "ITEM_COMBINE",
    "PATTERN_TRACE",
    "AUDIO_MATCH",
)

TRIGGER_TYPES = (
    "ON_PUZZLE_FAIL_COUNT",
    "ON_ENTER_AREA",
    "ON_COLLECT_ITEM",
    "ON_TIMER",
    "ON_WRONG_ITEM_USE",
)

PREFIX = {
    "hotspot": "hs_",
    "puzzle": "puz_",
    "jumpscare": "scare_",
    "item": "item_",
    "area": "area_",
    "flag": "flag_",
}

RE_SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")
RE_TEXT_KEY = re.compile(r"^txt_[a-z0-9_]+$")
RE_ANIM = re.compile(r"^anim_[a-z0-9_]+$")
RE_AUDIO = re.compile(r"^[a-z0-9_]+\.(ogg|mp3|wav)$")
RE_BUNDLE_URL = re.compile(r"^https://[A-Za-z0-9.\-]+/.+\.bundle$")
RE_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Tu vo nghia khi suy luan nguon cap co tien trinh tu ten co.
FLAG_STOPWORDS = {
    "flag", "da", "duoc", "xong", "roi", "la", "va", "cua", "cho",
    "solved", "done", "complete", "completed", "unlocked", "open", "opened",
}


# --------------------------------------------------------------------------
# MAU ASCII + BAO CAO
# --------------------------------------------------------------------------

class Palette:
    """Ma mau ANSI. Tu tat khi khong xuat ra terminal, khi co --no-color, hoac NO_COLOR."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def _w(self, code: str, text: str) -> str:
        return "\033[%sm%s\033[0m" % (code, text) if self.enabled else text

    def red(self, t):    return self._w("1;31", t)
    def yellow(self, t): return self._w("1;33", t)
    def green(self, t):  return self._w("1;32", t)
    def cyan(self, t):   return self._w("1;36", t)
    def bold(self, t):   return self._w("1", t)
    def dim(self, t):    return self._w("2", t)


class Report:
    """
    Gom ket qua kiem tra theo tung giai doan roi in mot lan, co mau.

    Voi strict=True, moi [CANH BAO] duoc NANG THANH [LOI] ngay tai cho - khong chi doi
    ma thoat o cuoi. Cong CI nhin vao ban in phai thay dung nhung gi no chan.
    """

    def __init__(self, palette: Palette, quiet: bool = False, strict: bool = False) -> None:
        self.p = palette
        self.quiet = quiet
        self.strict = strict
        self.errors = []
        self.warnings = []
        self._sections = []          # [(ten_giai_doan, [dong_da_to_mau])]
        self._current = None

    # -- dieu khien giai doan ------------------------------------------------
    def section(self, title: str) -> None:
        self._current = (title, [])
        self._sections.append(self._current)

    def _push(self, line: str) -> None:
        if self._current is None:
            self.section("KHAC")
        self._current[1].append(line)

    # -- ba muc do -----------------------------------------------------------
    def error(self, where: str, message: str, fix: str = "") -> None:
        self.errors.append((where, message))
        line = "  %s %s\n      %s" % (self.p.red("[LOI]"), self.p.bold(where), message)
        if fix:
            line += "\n      %s %s" % (self.p.dim("Cach sua:"), self.p.dim(fix))
        self._push(line)

    def warn(self, where: str, message: str, fix: str = "") -> None:
        if self.strict:
            # --strict: canh bao KHONG con la canh bao.
            self.errors.append((where, message))
            line = "  %s %s\n      %s" % (
                self.p.red("[LOI]"), self.p.bold(where),
                message + self.p.dim("  (nang tu [CANH BAO] vi dang chay --strict)"))
            if fix:
                line += "\n      %s %s" % (self.p.dim("Cach sua:"), self.p.dim(fix))
            self._push(line)
            return
        self.warnings.append((where, message))
        line = "  %s %s\n      %s" % (self.p.yellow("[CANH BAO]"), self.p.bold(where), message)
        if fix:
            line += "\n      %s %s" % (self.p.dim("Cach sua:"), self.p.dim(fix))
        self._push(line)

    def hint(self, where: str, message: str) -> None:
        """
        [i] GOI Y - khong phai ket luan, khong tinh vao ma thoat, khong bao gio duoc mot
        giai doan sau nao doc lai lam du kien dau vao. Dung cho phan suy luan tu ten.
        """
        self._push("  %s %s\n      %s\n      %s" % (
            self.p.cyan("[i]"), self.p.bold(where), message,
            self.p.dim("KHONG dung de ket luan kha giai - chi la goi y cho nguoi thiet ke.")))

    def ok(self, message: str) -> None:
        self._push("  %s %s" % (self.p.green("[OK]"), message))

    def info(self, message: str) -> None:
        self._push("  %s %s" % (self.p.cyan("[i]"), message))

    def plain(self, message: str) -> None:
        self._push("      %s" % self.p.dim(message))

    # -- ket xuat ------------------------------------------------------------
    def render(self, header: str) -> None:
        if self.quiet and not self.errors and not self.warnings:
            return
        out = []
        out.append(self.p.bold("=" * 78))
        out.append(self.p.bold("  " + header))
        out.append(self.p.bold("=" * 78))
        for title, lines in self._sections:
            if self.quiet and not any("[LOI]" in ln or "[CANH BAO]" in ln for ln in lines):
                continue
            out.append("")
            out.append(self.p.cyan("-- " + title + " " + "-" * max(0, 74 - len(title))))
            if not lines:
                out.append("  %s khong co muc nao de kiem." % self.p.dim("(trong)"))
            out.extend(lines)
        print("\n".join(out))

    def render_summary(self, strict: bool) -> int:
        n_err = len(self.errors)
        n_warn = len(self.warnings)
        print("")
        print(self.p.bold("=" * 78))
        if n_err and strict:
            verdict = self.p.red("THAT BAI (--strict: moi canh bao da duoc nang thanh loi).")
        elif n_err:
            verdict = self.p.red("THAT BAI - du lieu KHONG dung dong bo len build.")
        elif n_warn and strict:
            verdict = self.p.red("THAT BAI (che do --strict: canh bao duoc tinh la loi).")
        elif n_warn:
            verdict = self.p.yellow("DAT - nhung con canh bao can xu ly truoc khi khoa ban.")
        else:
            verdict = self.p.green("DAT - du lieu sach hoan toan.")
        print("  %s  |  %s: %d  |  %s: %d" % (
            verdict,
            self.p.red("[LOI]"), n_err,
            self.p.yellow("[CANH BAO]"), n_warn,
        ))
        print(self.p.bold("=" * 78))
        return 1 if (n_err or (strict and n_warn)) else 0


# --------------------------------------------------------------------------
# TIEN ICH KIEU DU LIEU
# --------------------------------------------------------------------------

def is_str(v) -> bool:
    return isinstance(v, str)


def is_int(v) -> bool:
    # bool la subclass cua int trong Python - phai loai tru tuong minh.
    return isinstance(v, int) and not isinstance(v, bool)


def is_bool(v) -> bool:
    return isinstance(v, bool)


def is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def is_list(v) -> bool:
    return isinstance(v, list)


def is_dict(v) -> bool:
    return isinstance(v, dict)


def str_list(container, key):
    """
    Lay mot truong dang mang chuoi mot cach AN TOAN.

    Neu du lieu ghi nham mot CHUOI vao cho cho mang (vd "required_flags": "flag_x"), vong
    for cua Python se duyet tung KY TU va de ra nhung "co tien trinh" ten la 'f', 'l', 'a'...
    Loi kieu du lieu that da duoc bao o GIAI DOAN 2-3 roi; o day chi can khong bia them rac.
    """
    value = container.get(key)
    if not is_list(value):
        return []
    return [v for v in value if is_str(v)]


def tokens_of(identifier: str) -> set:
    """Tach mot id snake_case thanh tap tu co nghia, bo tien to va tu vo nghia."""
    parts = identifier.split("_")
    return {t for t in parts if t and t not in FLAG_STOPWORDS and len(t) > 1}


def fmt_list(values, limit: int = 8) -> str:
    values = list(values)
    if not values:
        return "(khong co)"
    head = ", ".join(str(v) for v in values[:limit])
    return head if len(values) <= limit else head + ", ... (+%d)" % (len(values) - limit)


# --------------------------------------------------------------------------
# NAP DU LIEU
# --------------------------------------------------------------------------

def load_json(path: str, rep: Report, where: str):
    """Doc mot file JSON. Tra ve None neu khong doc/phan tich duoc (da ghi [LOI])."""
    if not os.path.isfile(path):
        rep.error(where, "Khong tim thay file: %s" % path,
                  "Kiem tra lai duong dan thu muc data truyen vao dong lenh.")
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        rep.error(where, "Khong doc duoc file: %s" % exc)
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        rep.error(
            where,
            "JSON hong o dong %d cot %d: %s" % (exc.lineno, exc.colno, exc.msg),
            "Mo file tai dong %d. Loi thuong gap: thua dau phay cuoi mang/doi tuong, "
            "thieu dau ngoac kep, hoac dung dau nhay don thay vi nhay kep." % exc.lineno,
        )
        return None


# --------------------------------------------------------------------------
# GIAI DOAN 2-3: CAU TRUC + RANG BUOC CO DIEU KIEN
# --------------------------------------------------------------------------

def check_bounds(bounds, rep: Report, where: str, has_visual_bounds: bool = False,
                 field: str = "bounds", touch_check: bool = True) -> bool:
    """GIAI DOAN 4. Tra ve True neu bounds hop le ve kieu du lieu."""
    if not is_dict(bounds):
        rep.error(where, "Truong '%s' phai la doi tuong {x, y, width, height}." % field)
        return False

    ok_types = True
    for key in ("x", "y", "width", "height"):
        if key not in bounds:
            rep.error(where, "Truong '%s' thieu khoa bat buoc '%s'." % (field, key))
            ok_types = False
        elif not is_int(bounds[key]):
            rep.error(where, "%s.%s phai la so nguyen, dang nhan '%r'." % (field, key, bounds[key]))
            ok_types = False
    if not ok_types:
        return False

    x, y = bounds["x"], bounds["y"]
    w, h = bounds["width"], bounds["height"]

    if w <= 0:
        rep.error(where, "%s.width = %d - phai lon hon 0." % (field, w))
    if h <= 0:
        rep.error(where, "%s.height = %d - phai lon hon 0." % (field, h))
    if x < 0 or y < 0:
        rep.error(where, "%s co toa do am (x=%d, y=%d). Goc (0,0) o GOC TREN-BEN TRAI."
                  % (field, x, y))

    if w > 0 and h > 0:
        if x + w > DESIGN_WIDTH:
            rep.error(
                where,
                "%s tran mep phai: x + width = %d > %d." % (field, x + w, DESIGN_WIDTH),
                "Giam width xuong %d hoac keo x ve %d." % (DESIGN_WIDTH - x, DESIGN_WIDTH - w),
            )
        if y + h > DESIGN_HEIGHT:
            rep.error(
                where,
                "%s tran mep duoi: y + height = %d > %d." % (field, y + h, DESIGN_HEIGHT),
                "Giam height xuong %d hoac keo y ve %d." % (DESIGN_HEIGHT - y, DESIGN_HEIGHT - h),
            )
        if touch_check:
            check_touch_size(w, h, rep, where, has_visual_bounds)
    return True


def check_touch_size(w: int, h: int, rep: Report, where: str, has_visual_bounds: bool) -> None:
    """
    GIAI DOAN 4 - nguong vung cham hai muc.

      canh < 88  px @1920 -> [LOI]       : duoi san cung, khong ngoai le
      canh < 120 px @1920 -> [CANH BAO]  : tru khi hotspot khai bao visual_bounds
    """
    small_edge = min(w, h)

    if small_edge < HARD_MIN_TOUCH_SIZE:
        rep.error(
            where,
            "Vung cham %dx%d co canh %d px @1920 - DUOI san cung %d px. Quy doi ra may that "
            "chi con khoang %d-%d pt, thap hon 44 pt cua Apple HIG va 48 dp cua Android; "
            "ngon tay nguoi lon khong bam trung duoc mot cach on dinh."
            % (w, h, small_edge, HARD_MIN_TOUCH_SIZE,
               int(small_edge * 0.33), int(small_edge * 0.49)),
            "No 'bounds' len it nhat %d px moi canh (nen %d px). Neu sprite thuc su nho, "
            "cu no bounds va khai bao 'visual_bounds' bang dung vung ve - vung cham duoc "
            "phep lon hon hinh ve."
            % (HARD_MIN_TOUCH_SIZE, MIN_TOUCH_SIZE),
        )
        return

    if small_edge < MIN_TOUCH_SIZE:
        if has_visual_bounds:
            return          # da khai bao visual_bounds = co chu dich, khong bao lai
        rep.warn(
            where,
            "Vung cham %dx%d co canh %d px @1920, chua dat nguong khuyen nghi %d px "
            "(khoang %d-%d pt tren may that, sat nguong 44 pt cua Apple HIG)."
            % (w, h, small_edge, MIN_TOUCH_SIZE,
               int(small_edge * 0.33), int(small_edge * 0.49)),
            "No 'bounds' len >= %d px moi canh - vung cham khong bat buoc trung voi hinh ve. "
            "Neu da co chu dich giu nho, them 'visual_bounds' bang dung vung ve cua sprite "
            "de khai bao ro y do (khi do canh bao nay tat)."
            % MIN_TOUCH_SIZE,
        )


def check_visual_bounds(hs, rep: Report, where: str) -> None:
    """
    GIAI DOAN 4 - visual_bounds (vung ve that cua sprite) phai nam TRON trong bounds
    (vung cham mo rong). Vung ve loi ra ngoai vung cham nghia la co phan hinh nguoi choi
    nhin thay, bam vao, ma khong co gi xay ra.
    """
    vb = hs.get("visual_bounds")
    if vb is None:
        return
    if not check_bounds(vb, rep, where, field="visual_bounds", touch_check=False):
        return

    bounds = hs.get("bounds")
    if not is_dict(bounds) or not all(is_int(bounds.get(k)) for k in ("x", "y", "width", "height")):
        return          # loi bounds da duoc bao o cho khac

    bx, by = bounds["x"], bounds["y"]
    bx2, by2 = bx + bounds["width"], by + bounds["height"]
    vx, vy = vb["x"], vb["y"]
    vx2, vy2 = vx + vb["width"], vy + vb["height"]

    over = []
    if vx < bx:
        over.append("trai %d px" % (bx - vx))
    if vy < by:
        over.append("tren %d px" % (by - vy))
    if vx2 > bx2:
        over.append("phai %d px" % (vx2 - bx2))
    if vy2 > by2:
        over.append("duoi %d px" % (vy2 - by2))

    if over:
        rep.error(
            where,
            "visual_bounds (%d,%d %dx%d) loi ra ngoai bounds (%d,%d %dx%d) o phia %s. "
            "Phan hinh ve nam ngoai vung cham la phan nguoi choi nhin thay, bam vao, "
            "va khong co gi xay ra."
            % (vx, vy, vb["width"], vb["height"],
               bx, by, bounds["width"], bounds["height"], ", ".join(over)),
            "visual_bounds phai nam TRON trong bounds. Hoac no bounds bao het vung ve, "
            "hoac thu visual_bounds lai cho dung phan sprite thuc su ve.",
        )
    elif vb["width"] > bounds["width"] or vb["height"] > bounds["height"]:
        rep.error(where, "visual_bounds lon hon bounds - nguoc voi y nghia cua truong nay "
                         "(vung ve phai nho hon hoac bang vung cham).")


def check_hotspot(hs, rep: Report, area_id: str, index: int) -> bool:
    """GIAI DOAN 2+3 cho mot hotspot. Tra ve True neu du tot de di tiep."""
    where = "%s / hotspots[%d]" % (area_id, index)
    if not is_dict(hs):
        rep.error(where, "Phan tu hotspot phai la doi tuong JSON.")
        return False

    hs_id = hs.get("id")
    if not is_str(hs_id):
        rep.error(where, "Thieu truong bat buoc 'id' (chuoi).")
        return False
    where = "%s / %s" % (area_id, hs_id)

    if not hs_id.startswith(PREFIX["hotspot"]):
        rep.error(where, "Id hotspot phai bat dau bang tien to '%s'." % PREFIX["hotspot"])
    if not RE_SNAKE.match(hs_id):
        rep.error(where, "Id '%s' khong dung snake_case khong dau." % hs_id)

    if "bounds" not in hs:
        rep.error(where, "Thieu truong bat buoc 'bounds'.")
    else:
        check_bounds(hs["bounds"], rep, where,
                     has_visual_bounds=is_dict(hs.get("visual_bounds")))
        check_visual_bounds(hs, rep, where)

    action = hs.get("action_type")
    if not is_str(action):
        rep.error(where, "Thieu truong bat buoc 'action_type' (chuoi).")
        return False
    if action not in ACTION_TYPES:
        rep.error(
            where,
            "action_type '%s' khong thuoc tap cho phep." % action,
            "Chon mot trong: %s" % ", ".join(ACTION_TYPES),
        )
        return False

    # ---- rang buoc co dieu kien theo action_type ---------------------------
    if action == "ZOOM_PUZZLE":
        if not is_str(hs.get("target_puzzle_id")):
            rep.error(where, "ZOOM_PUZZLE bat buoc co 'target_puzzle_id' tro toi mot puzzle "
                             "trong CUNG file area.")

    elif action == "COLLECT_ITEM":
        if not is_str(hs.get("item_id")):
            rep.error(where, "COLLECT_ITEM bat buoc co 'item_id' (chuoi).")
        if "required_item" not in hs:
            rep.error(where, "COLLECT_ITEM bat buoc khai bao 'required_item' - dat null "
                             "neu nhat duoc ngay khong can dieu kien.")
        elif hs["required_item"] is not None and not is_str(hs["required_item"]):
            rep.error(where, "'required_item' phai la item_id hoac null.")

    elif action == "USE_ITEM":
        req = hs.get("required_item")
        if not is_str(req):
            rep.error(where, "USE_ITEM bat buoc co 'required_item' KHAC null - "
                             "phai noi ro dung vat pham nao.")
        # Hieu ung hop le cua USE_ITEM: trao vat pham MOI, mo cau do, hoac - dang hay gap
        # nhat o Chuong 1 - chi de lai mot co tien trinh ("dat vat pham vao cho" ma khong
        # tieu huy vat pham, khong trao gi moi). check_use_item_noop() bao gom ca ba.
        check_use_item_noop(hs, rep, where)

    elif action == "CHANGE_AREA":
        if not is_str(hs.get("target_area_id")):
            rep.error(where, "CHANGE_AREA bat buoc co 'target_area_id' tro toi mot area "
                             "co trong chapter manifest.")

    elif action in ("EXAMINE", "DIALOGUE"):
        tk = hs.get("text_key")
        if not is_str(tk):
            rep.error(where, "%s bat buoc co 'text_key' (khoa localization, vd "
                             "'txt_examine_ban_tho')." % action)
        elif not RE_TEXT_KEY.match(tk):
            rep.error(where, "text_key '%s' sai quy uoc - phai khop ^txt_[a-z0-9_]+$." % tk)
        for forbidden in ("item_id", "required_item", "target_puzzle_id", "target_area_id"):
            if forbidden in hs:
                rep.error(where, "%s khong duoc mang truong '%s'." % (action, forbidden))

    if action != "CHANGE_AREA" and "target_area_id" in hs:
        rep.error(where, "Chi CHANGE_AREA moi duoc mang 'target_area_id'.")

    for key in ("item_id", "required_item"):
        val = hs.get(key)
        if is_str(val) and not val.startswith(PREFIX["item"]):
            rep.error(where, "%s = '%s' phai bat dau bang tien to '%s'."
                      % (key, val, PREFIX["item"]))

    gf = hs.get("grants_flag")
    if gf is not None and not is_str(gf):
        rep.error(where, "'grants_flag' phai la flag_id hoac null, dang nhan %r." % (gf,))
    elif is_str(gf) and not gf.startswith(PREFIX["flag"]):
        rep.error(where, "grants_flag = '%s' phai bat dau bang tien to '%s'."
                  % (gf, PREFIX["flag"]))

    # ---- required_flags ----------------------------------------------------
    rf = hs.get("required_flags")
    if rf is not None and not is_list(rf):
        rep.error(where, "'required_flags' phai la mang flag_id (mang rong = khong dieu kien).")
        rf = []
    rf = [f for f in (rf or [])]
    for flag in rf:
        if not is_str(flag) or not flag.startswith(PREFIX["flag"]):
            rep.error(where, "required_flags chua gia tri khong hop le: %r - phai la chuoi "
                             "bat dau bang '%s'." % (flag, PREFIX["flag"]))
    if len(set(f for f in rf if is_str(f))) != len([f for f in rf if is_str(f)]):
        rep.error(where, "'required_flags' co phan tu trung nhau.")

    # ---- fallback_text_key: giai thich khi nguoi choi bi chan --------------
    fbk = hs.get("fallback_text_key")
    if fbk is not None and not is_str(fbk):
        rep.error(where, "'fallback_text_key' phai la text_key (chuoi).")
    elif is_str(fbk) and not RE_TEXT_KEY.match(fbk):
        rep.error(where, "fallback_text_key '%s' sai quy uoc - phai khop ^txt_[a-z0-9_]+$." % fbk)

    gated_by_item = is_str(hs.get("required_item"))
    gated_by_flags = bool([f for f in rf if is_str(f)])
    if (gated_by_item or gated_by_flags) and not is_str(fbk):
        why = []
        if gated_by_item:
            why.append("required_item = '%s'" % hs.get("required_item"))
        if gated_by_flags:
            why.append("required_flags = %s" % fmt_list([f for f in rf if is_str(f)]))
        rep.warn(
            where,
            "Hotspot co dieu kien (%s) nhung khong co 'fallback_text_key'. Nguoi choi bam "
            "trung ma chua du dieu kien se khong nhan duoc loi giai thich nao - man hinh "
            "im lang, ho tuong hotspot hong va bo qua no." % "; ".join(why),
            "Them \"fallback_text_key\": \"txt_...\" voi mot cau nhac huong ve thu con thieu "
            "(vd \"Then cua nay can mot vat gi do vua khop khe mong.\").",
        )
    return True


def check_use_item_noop(hs, rep: Report, where: str) -> None:
    """
    GIAI DOAN 3 - hotspot USE_ITEM khong sinh ra hieu ung nao DOC DUOC BANG MAY.

    Mot hotspot USE_ITEM chi thuc su lam gi do khi no:
      - bat mot co tien trinh   (grants_flag), hoac
      - mo mot cau do           (target_puzzle_id), hoac
      - mo duong sang khu vuc   (target_area_id), hoac
      - trao mot vat pham MOI   (item_id KHAC required_item).

    Neu item_id trung dung required_item va khong co gi khac, hotspot nay chi "tra lai
    dung cai vua lay ra": trang thai may sau khi bam y het truoc khi bam. Nguoi choi thay
    hoat anh, nhung khong mot dieu kien nao trong chuong tien them mot buoc - va mo phong
    kha giai se dung lai ngay o day.
    """
    req = hs.get("required_item")
    item_id = hs.get("item_id")

    effects = []
    if is_str(hs.get("grants_flag")):
        effects.append("grants_flag")
    if is_str(hs.get("target_puzzle_id")):
        effects.append("target_puzzle_id")
    if is_str(hs.get("target_area_id")):
        effects.append("target_area_id")
    if is_str(item_id) and item_id != req:
        effects.append("item_id moi")

    if effects:
        return

    if is_str(item_id) and is_str(req) and item_id == req:
        detail = ("item_id = required_item = '%s' (dat vat pham vao roi nhan lai dung no)"
                  % item_id)
    elif is_str(item_id):
        detail = "item_id = '%s' khong phai vat pham moi" % item_id
    else:
        detail = "khong co 'item_id' nao duoc trao"

    rep.error(
        where,
        "Hotspot USE_ITEM nay KHONG LAM GI CA: %s, khong 'grants_flag', khong "
        "'target_puzzle_id', khong 'target_area_id'. Khong mot bit trang thai nao doi sau "
        "khi nguoi choi dung vat pham, nen ca engine lan trinh kiem deu khong biet viec "
        "dung vat pham da xay ra - moi khu vuc/hotspot doi 'da dat vat pham' se ket cung."
        % detail,
        "Them \"grants_flag\": \"flag_<viec_vua_lam>\" (cach dung nhat, vi unlock_condition "
        "doc duoc no), hoac tro 'target_puzzle_id' toi cau do duoc mo ra, hoac trao mot "
        "'item_id' KHAC voi 'required_item'.",
    )


def check_puzzle(pz, rep: Report, area_id: str, index: int) -> bool:
    where = "%s / puzzles[%d]" % (area_id, index)
    if not is_dict(pz):
        rep.error(where, "Phan tu puzzle phai la doi tuong JSON.")
        return False

    pz_id = pz.get("id")
    if not is_str(pz_id):
        rep.error(where, "Thieu truong bat buoc 'id' (chuoi).")
        return False
    where = "%s / %s" % (area_id, pz_id)

    if not pz_id.startswith(PREFIX["puzzle"]):
        rep.error(where, "Id puzzle phai bat dau bang tien to '%s'." % PREFIX["puzzle"])
    if not RE_SNAKE.match(pz_id):
        rep.error(where, "Id '%s' khong dung snake_case khong dau." % pz_id)

    ptype = pz.get("type")
    if not is_str(ptype):
        rep.error(where, "Thieu truong bat buoc 'type'.")
    elif ptype not in PUZZLE_TYPES:
        rep.error(where, "puzzles[].type = '%s' khong thuoc tap cho phep." % ptype,
                  "Chon mot trong: %s" % ", ".join(PUZZLE_TYPES))

    sol = pz.get("solution")
    if not is_list(sol):
        rep.error(where, "Thieu truong bat buoc 'solution' (mang so nguyen).")
    elif not sol:
        rep.error(where, "'solution' rong - cau do khong the giai duoc.")
    elif not all(is_int(v) for v in sol):
        rep.error(where, "'solution' chi duoc chua so nguyen.")
    else:
        # Rang buoc theo tung the loai cau do.
        if ptype in ("SEQUENCE_ORDER", "PATTERN_TRACE", "ITEM_COMBINE") and len(set(sol)) != len(sol):
            dup = sorted({v for v in sol if sol.count(v) > 1})
            rep.error(where, "%s co 'solution' lap phan tu %s - loi giai phai la mot hoan vi "
                             "cac buoc phan biet." % (ptype, fmt_list(dup)))
        if ptype == "SLIDING_TILE":
            if len(sol) not in (9, 16):
                rep.error(where, "SLIDING_TILE phai co dung 9 (khung 3x3) hoac 16 (khung 4x4) "
                                 "phan tu, dang co %d." % len(sol))
            if sol.count(0) != 1:
                rep.error(where, "SLIDING_TILE phai co dung MOT o trong ky hieu 0, "
                                 "dang dem duoc %d." % sol.count(0))
            if len(set(sol)) != len(sol):
                rep.error(where, "SLIDING_TILE co manh ghep trung nhau trong 'solution'.")

    if "reward_item_id" not in pz:
        rep.error(where, "Thieu truong bat buoc 'reward_item_id' (item_id hoac null).")
    else:
        rid = pz["reward_item_id"]
        if rid is not None and not is_str(rid):
            rep.error(where, "'reward_item_id' phai la item_id hoac null.")
        elif is_str(rid) and not rid.startswith(PREFIX["item"]):
            rep.error(where, "reward_item_id = '%s' phai bat dau bang '%s'." % (rid, PREFIX["item"]))

    if "wrong_action_jumpscare" not in pz:
        rep.error(where, "Thieu truong bat buoc 'wrong_action_jumpscare' (scare_id hoac null).")
    else:
        waj = pz["wrong_action_jumpscare"]
        if waj is not None and not is_str(waj):
            rep.error(where, "'wrong_action_jumpscare' phai la scare_id hoac null.")
        elif is_str(waj) and not waj.startswith(PREFIX["jumpscare"]):
            rep.error(where, "wrong_action_jumpscare = '%s' phai bat dau bang '%s'."
                      % (waj, PREFIX["jumpscare"]))

    ri = pz.get("required_items")
    if ri is not None and not is_list(ri):
        rep.error(where, "'required_items' phai la mang item_id.")
    elif is_list(ri):
        for item in ri:
            if not is_str(item) or not item.startswith(PREFIX["item"]):
                rep.error(where, "required_items chua gia tri khong hop le: %r" % (item,))
        names = [i for i in ri if is_str(i)]
        if len(set(names)) != len(names):
            rep.error(where, "'required_items' co vat pham lap lai.")

    gf = pz.get("grants_flag")
    if gf is not None and not is_str(gf):
        rep.error(where, "'grants_flag' phai la flag_id hoac null, dang nhan %r." % (gf,))
    elif is_str(gf) and not gf.startswith(PREFIX["flag"]):
        rep.error(where, "grants_flag = '%s' phai bat dau bang tien to '%s'."
                  % (gf, PREFIX["flag"]))
    return True


def check_jumpscare(js, rep: Report, area_id: str, index: int) -> bool:
    where = "%s / jumpscares[%d]" % (area_id, index)
    if not is_dict(js):
        rep.error(where, "Phan tu jumpscare phai la doi tuong JSON.")
        return False

    js_id = js.get("id")
    if not is_str(js_id):
        rep.error(where, "Thieu truong bat buoc 'id' (chuoi).")
        return False
    where = "%s / %s" % (area_id, js_id)

    if not js_id.startswith(PREFIX["jumpscare"]):
        rep.error(where, "Id jumpscare phai bat dau bang tien to '%s'." % PREFIX["jumpscare"])
    if not RE_SNAKE.match(js_id):
        rep.error(where, "Id '%s' khong dung snake_case khong dau." % js_id)

    trig = js.get("trigger_type")
    if not is_str(trig):
        rep.error(where, "Thieu truong bat buoc 'trigger_type'.")
        return True
    if trig not in TRIGGER_TYPES:
        rep.error(where, "trigger_type '%s' khong thuoc tap cho phep." % trig,
                  "Chon mot trong: %s" % ", ".join(TRIGGER_TYPES))
        return True

    # ---- rang buoc co dieu kien theo trigger_type --------------------------
    if trig == "ON_PUZZLE_FAIL_COUNT":
        mf = js.get("max_fails")
        if mf is None:
            rep.error(where, "ON_PUZZLE_FAIL_COUNT bat buoc co 'max_fails'.",
                      "Them \"max_fails\": 3 - so lan giai sai lien tiep truoc khi cu doa ban.")
        elif not is_int(mf):
            rep.error(where, "'max_fails' phai la so nguyen, dang nhan %r." % (mf,))
        elif mf < 1:
            rep.error(where, "'max_fails' = %d - phai la so nguyen >= 1." % mf)
    else:
        if "max_fails" in js:
            rep.error(where, "trigger_type '%s' KHONG duoc mang 'max_fails' - "
                             "truong nay chi thuoc ve ON_PUZZLE_FAIL_COUNT." % trig)

    # delay_sec = do tre tu luc dieu kien kich hoat thoa man den luc cu doa ban.
    # BAT BUOC voi ON_TIMER (o do no la chinh dinh nghia cua trigger); TUY CHON o cac
    # trigger khac, noi no la do tre nhip (vd ban 350 ms sau khi vat pham vao tui do).
    if "delay_sec" in js:
        ds = js["delay_sec"]
        if not is_num(ds):
            rep.error(where, "'delay_sec' phai la so, dang nhan %r." % (ds,))
        elif ds < 0:
            rep.error(where, "'delay_sec' = %r - phai lon hon hoac bang 0." % (ds,))
        elif ds == 0 and trig == "ON_TIMER":
            rep.warn(where, "'delay_sec' = 0 tren ON_TIMER - cu doa ban ngay khi vua vao khu "
                            "vuc, tuc dung y nghia cua ON_ENTER_AREA chu khong phai ON_TIMER.",
                     "Dat delay_sec > 0, hoac doi trigger_type sang ON_ENTER_AREA cho dung ten.")
    elif trig == "ON_TIMER":
        rep.error(where, "ON_TIMER BAT BUOC co 'delay_sec'. Thieu no thi thoi diem ban cu doa "
                         "khong xac dinh: moi may, moi ban build se ban mot kieu, va khong ai "
                         "kiem thu lai duoc mot loi khieu nai.",
                  "Them \"delay_sec\": <so giay dung yen trong khu vuc truoc khi ban>, vd 25.")

    if trig == "ON_COLLECT_ITEM":
        tii = js.get("trigger_item_id")
        if not is_str(tii):
            rep.error(where, "ON_COLLECT_ITEM BAT BUOC co 'trigger_item_id' - phai noi ro NHAT "
                             "VAT PHAM NAO thi cu doa ban. Thieu no thi engine khong co dieu "
                             "kien nao de kich hoat, cu doa nam chet trong du lieu.",
                      "Them \"trigger_item_id\": \"item_...\" tro toi vat pham gay ra cu doa.")
        elif not tii.startswith(PREFIX["item"]):
            rep.error(where, "trigger_item_id = '%s' phai bat dau bang tien to '%s'."
                      % (tii, PREFIX["item"]))
    elif trig == "ON_WRONG_ITEM_USE":
        tii = js.get("trigger_item_id")
        if is_str(tii) and not tii.startswith(PREFIX["item"]):
            rep.error(where, "trigger_item_id = '%s' phai bat dau bang tien to '%s'."
                      % (tii, PREFIX["item"]))
    elif "trigger_item_id" in js:
        rep.error(where, "Chi ON_COLLECT_ITEM / ON_WRONG_ITEM_USE moi duoc mang "
                         "'trigger_item_id'.")

    if "cooldown_sec" in js:
        cd = js["cooldown_sec"]
        if not is_num(cd):
            rep.error(where, "'cooldown_sec' phai la so, dang nhan %r." % (cd,))
        elif cd < 0:
            rep.error(where, "'cooldown_sec' = %r - phai lon hon hoac bang 0." % (cd,))
        if js.get("cooldown_exempt") is True:
            rep.error(where, "Khai bao dong thoi 'cooldown_sec' va \"cooldown_exempt\": true - "
                             "mau thuan, khong biet cu doa nay co luat nghi hay khong.",
                      "Giu mot trong hai: cooldown_sec neu co luat nghi, cooldown_exempt neu "
                      "duoc mien tru.")
    elif trig in ("ON_ENTER_AREA", "ON_TIMER") and js.get("cooldown_exempt") is not True:
        rep.warn(where, "Cu doa loai '%s' co the ban lai nhieu lan nhung khong khai bao "
                        "'cooldown_sec'. Doa lien tiep lam nguoi choi quen so va mat sach "
                        "hieu qua." % trig,
                 "Them \"cooldown_sec\": <so giay nghi toi thieu>, vd 90. Neu cu doa nay duoc "
                 "MIEN TRU luat nghi mot cach co chu dich (dread scare nhe, khong transient, "
                 "khong flash, khong haptic), dat \"cooldown_exempt\": true kem 'ghi_chu_vi' "
                 "neu ro can cu - khai bao y do bang du lieu, dung bang ghi chu suong.")

    if "cooldown_exempt" in js and not is_bool(js["cooldown_exempt"]):
        rep.error(where, "'cooldown_exempt' phai la true hoac false.")

    # SIET CHAT (khong noi long): mien tru cooldown khong duoc dung lam cua sau cho mot cu
    # doa xung. 04_horror.md muc 2.8.2 dinh nghia luat mien tru la: impulse == false VA
    # screen_flash == false VA camera_punch_pct == 0 VA haptic_pattern_at_0ms == null.
    # Trong hop dong du lieu hien tai, chi 'screen_flash' la doc duoc bang may - nen day la
    # dieu kien CAN duy nhat may kiem duoc, va no phai duoc kiem. Mot cu doa vua chop man
    # vua tu nhan mien tru cooldown la mot impulse scare ban lai khong gioi han: dung cai
    # ma luat cooldown sinh ra de chan.
    if js.get("cooldown_exempt") is True and js.get("screen_flash") is True:
        rep.error(where, "Khai bao \"cooldown_exempt\": true nhung 'screen_flash' = true - "
                         "mien tru cooldown chi danh cho dread scare (khong transient, khong "
                         "flash, khong punch, khong haptic o moc 0 ms) theo 04_horror.md muc "
                         "2.8.2. Mot cu doa co chop man la impulse scare, va impulse scare "
                         "chiu TOAN BO luat nghi 90 s.",
                  "Hoac dat \"screen_flash\": false neu day that su la cu doa nen, hoac bo "
                  "\"cooldown_exempt\" va khai bao \"cooldown_sec\": 90.")

    audio = js.get("audio_asset")
    if not is_str(audio):
        rep.error(where, "Thieu truong bat buoc 'audio_asset'.")
    elif not RE_AUDIO.match(audio):
        rep.warn(where, "audio_asset '%s' sai quy uoc ten file (mong doi <ten>.ogg/.mp3/.wav)."
                 % audio)

    anim = js.get("sprite_animation")
    if not is_str(anim):
        rep.error(where, "Thieu truong bat buoc 'sprite_animation'.")
    elif not RE_ANIM.match(anim):
        rep.error(where, "sprite_animation '%s' phai khop ^anim_[a-z0-9_]+$." % anim)

    if "screen_flash" not in js:
        rep.error(where, "Thieu truong bat buoc 'screen_flash' (true/false).")
    elif not is_bool(js["screen_flash"]):
        rep.error(where, "'screen_flash' phai la true hoac false.")
    return True


# --------------------------------------------------------------------------
# GIAI DOAN 5: HOTSPOT CHONG LAN
# --------------------------------------------------------------------------

def rect_overlap(a, b):
    """Tra ve (w, h) phan giao, hoac None neu hai hinh chu nhat roi nhau."""
    ax1, ay1 = a["x"], a["y"]
    ax2, ay2 = ax1 + a["width"], ay1 + a["height"]
    bx1, by1 = b["x"], b["y"]
    bx2, by2 = bx1 + b["width"], by1 + b["height"]
    ow = min(ax2, bx2) - max(ax1, bx1)
    oh = min(ay2, by2) - max(ay1, by1)
    if ow > 0 and oh > 0:
        return ow, oh
    return None


def check_overlaps(area_id: str, hotspots, rep: Report) -> None:
    usable = [
        hs for hs in hotspots
        if is_dict(hs) and is_str(hs.get("id")) and is_dict(hs.get("bounds"))
        and all(is_int(hs["bounds"].get(k)) for k in ("x", "y", "width", "height"))
        and hs["bounds"]["width"] > 0 and hs["bounds"]["height"] > 0
    ]
    found = 0
    for i in range(len(usable)):
        for j in range(i + 1, len(usable)):
            a, b = usable[i], usable[j]
            ov = rect_overlap(a["bounds"], b["bounds"])
            if ov:
                found += 1
                ow, oh = ov
                rep.error(
                    "%s / %s <-> %s" % (area_id, a["id"], b["id"]),
                    "Hai vung cham chong lan nhau %dx%d px (dien tich %d px2). "
                    "Nguoi choi bam vao vung giao se khong doan duoc hanh dong nao chay."
                    % (ow, oh, ow * oh),
                    "Thu nho hoac doi cho mot trong hai bounds: %s=%r, %s=%r."
                    % (a["id"], a["bounds"], b["id"], b["bounds"]),
                )
    if not found and usable:
        rep.ok("%s: %d vung cham, khong co cap nao chong lan." % (area_id, len(usable)))


# --------------------------------------------------------------------------
# MO HINH CHUONG - gom du lieu da chuan hoa de cac giai doan sau dung chung
# --------------------------------------------------------------------------

class Chapter:
    def __init__(self):
        self.chapter_id = None
        self.start_area_id = None
        self.area_order = []
        self.areas = {}           # area_id -> du lieu file area
        self.unlock = {}          # area_id -> unlock_condition (dict da chuan hoa)
        self.items = {}           # item_id -> muc trong item_catalog
        self.hotspots = {}        # hs_id -> (area_id, hotspot)
        self.puzzles = {}         # puz_id -> (area_id, puzzle)
        self.jumpscares = {}      # scare_id -> (area_id, jumpscare)
        self.flag_producers = {}  # flag_id -> list[(kind, id, area_id, how)]
        self.exported_flags = []  # co ban giao sang chuong sau, khai bao o manifest

    def area_hotspots(self, area_id):
        area = self.areas.get(area_id) or {}
        return [hs for hs in area.get("hotspots", []) if is_dict(hs) and is_str(hs.get("id"))]

    def final_area_id(self):
        return self.area_order[-1] if self.area_order else None


def normalize_unlock(raw, area_id: str, rep: Report):
    """Chuan hoa unlock_condition cua manifest ve dang {type, items, flags, from}."""
    if not is_dict(raw):
        rep.warn("chapter_01.json / %s" % area_id,
                 "Thieu 'unlock_condition' - trinh kiem coi khu vuc nay mo tu do.",
                 "Khai bao unlock_condition voi type NONE / ALL_OF / ANY_OF.")
        return {"type": "NONE", "items": [], "flags": [], "from": None, "entry": None}

    utype = raw.get("type", "ALL_OF")
    if utype not in ("NONE", "ALL_OF", "ANY_OF"):
        rep.error("chapter_01.json / %s" % area_id,
                  "unlock_condition.type = '%s' khong hop le." % utype,
                  "Chon NONE, ALL_OF hoac ANY_OF.")
        utype = "ALL_OF"

    items = str_list(raw, "required_items")
    flags = str_list(raw, "required_flags")
    return {
        "type": utype,
        "items": items,
        "flags": flags,
        "from": raw.get("from_area_id"),
        "entry": raw.get("entry_hotspot_id"),
    }


# --------------------------------------------------------------------------
# GIAI DOAN 6: DINH DANH DUY NHAT TOAN CHUONG
# --------------------------------------------------------------------------

def check_unique_ids(ch: Chapter, rep: Report) -> None:
    """Moi id phai duy nhat tren TOAN CHUONG, khong chi trong mot file."""
    seen = {}          # id -> list[(loai, noi khai bao)]
    dup_count = 0

    def declare(identifier, kind, where):
        seen.setdefault(identifier, []).append((kind, where))

    for area_id in ch.areas:
        declare(area_id, "area", "chapter_01.json / area_order")
    for item_id in ch.items:
        declare(item_id, "item", "chapter_01.json / item_catalog")
    for hs_id, (area_id, _) in ch.hotspots.items():
        declare(hs_id, "hotspot", "%s.json" % area_id)
    for pz_id, (area_id, _) in ch.puzzles.items():
        declare(pz_id, "puzzle", "%s.json" % area_id)
    for js_id, (area_id, _) in ch.jumpscares.items():
        declare(js_id, "jumpscare", "%s.json" % area_id)

    for identifier, decls in sorted(seen.items()):
        if len(decls) > 1:
            dup_count += 1
            rep.error(
                "id '%s'" % identifier,
                "Dinh danh bi khai bao %d lan: %s"
                % (len(decls), "; ".join("%s tai %s" % (k, w) for k, w in decls)),
                "Moi id phai duy nhat tren toan chuong. Doi ten mot trong cac ban trung.",
            )
    if not dup_count:
        rep.ok("%d dinh danh (area/item/hotspot/puzzle/jumpscare) deu duy nhat toan chuong."
               % len(seen))


def check_duplicate_within_files(ch_areas, rep: Report) -> None:
    """Bat truong hop mot file area khai bao hai phan tu cung id (bi ghi de am tham)."""
    for area_id, area in ch_areas.items():
        for coll in ("hotspots", "puzzles", "jumpscares"):
            counts = defaultdict(int)
            for entry in area.get(coll, []) or []:
                if is_dict(entry) and is_str(entry.get("id")):
                    counts[entry["id"]] += 1
            for identifier, n in sorted(counts.items()):
                if n > 1:
                    rep.error("%s / %s" % (area_id, coll),
                              "Id '%s' xuat hien %d lan trong cung mot mang." % (identifier, n))


# --------------------------------------------------------------------------
# GIAI DOAN 7: THAM CHIEU CHEO
# --------------------------------------------------------------------------

def check_cross_references(ch: Chapter, rep: Report) -> None:
    broken = 0

    # -- 7.1 hotspot -> puzzle / area / item --------------------------------
    for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
        where = "%s / %s" % (area_id, hs_id)

        tpid = hs.get("target_puzzle_id")
        if is_str(tpid):
            if tpid not in ch.puzzles:
                broken += 1
                rep.error(where, "target_puzzle_id = '%s' khong ton tai o bat ky dau trong chuong."
                          % tpid,
                          "Kiem tra chinh ta, hoac khai bao puzzle do trong mang 'puzzles' "
                          "cua file area nay.")
            elif ch.puzzles[tpid][0] != area_id:
                broken += 1
                rep.error(where, "target_puzzle_id = '%s' nam o khu vuc '%s', khong phai '%s'. "
                                 "Hop dong bat buoc puzzle phai o CUNG file area voi hotspot."
                          % (tpid, ch.puzzles[tpid][0], area_id))

        taid = hs.get("target_area_id")
        if is_str(taid) and taid not in ch.areas:
            broken += 1
            rep.error(where, "target_area_id = '%s' khong co trong chapter manifest." % taid,
                      "Them khu vuc vao 'areas'/'area_order' cua chapter_01.json, hoac sua "
                      "lai id cho dung.")

        for key in ("item_id", "required_item"):
            val = hs.get(key)
            if is_str(val) and val not in ch.items:
                broken += 1
                rep.error(where, "%s = '%s' khong co trong 'item_catalog' cua chapter manifest."
                          % (key, val),
                          "Moi vat pham phai duoc khai bao mot lan trong chapter_01.json / "
                          "item_catalog truoc khi duoc tham chieu.")

        # Co tien trinh khong co nguon cap da duoc GIAI DOAN 7a bao mot lan, kem dia chi
        # moi noi tham chieu - khong bao lai o day de khoi nhan doi so luong loi.

        fbk = hs.get("fallback_text_key")
        if is_str(fbk) and fbk == hs.get("text_key"):
            rep.warn(where, "fallback_text_key trung y het text_key ('%s') - nguoi choi nhan "
                            "cung mot cau du da du dieu kien hay chua, nen khong biet minh "
                            "con thieu gi." % fbk,
                     "Tach hai khoa: text_key la ket qua khi lam duoc, fallback_text_key la "
                     "loi nhac khi con thieu dieu kien.")


    # -- 7.2 puzzle -> jumpscare / item -------------------------------------
    for pz_id, (area_id, pz) in sorted(ch.puzzles.items()):
        where = "%s / %s" % (area_id, pz_id)

        waj = pz.get("wrong_action_jumpscare")
        if is_str(waj):
            if waj not in ch.jumpscares:
                broken += 1
                rep.error(where, "wrong_action_jumpscare = '%s' khong ton tai trong chuong." % waj)
            elif ch.jumpscares[waj][0] != area_id:
                broken += 1
                rep.error(where, "wrong_action_jumpscare = '%s' nam o khu vuc '%s', khong phai "
                                 "'%s'. Hop dong bat buoc jumpscare phai o CUNG file area."
                          % (waj, ch.jumpscares[waj][0], area_id))
            else:
                trig = ch.jumpscares[waj][1].get("trigger_type")
                if trig not in ("ON_PUZZLE_FAIL_COUNT", "ON_WRONG_ITEM_USE"):
                    rep.warn(where, "Cau do tro toi jumpscare '%s' nhung cu doa do co "
                                    "trigger_type = '%s' - no se khong bao gio ban vi giai sai."
                             % (waj, trig),
                             "Doi trigger_type sang ON_PUZZLE_FAIL_COUNT, hoac bo tham chieu.")

        rid = pz.get("reward_item_id")
        if is_str(rid) and rid not in ch.items:
            broken += 1
            rep.error(where, "reward_item_id = '%s' khong co trong 'item_catalog'." % rid)

        for item in str_list(pz, "required_items"):
            if item not in ch.items:
                broken += 1
                rep.error(where, "required_items chua '%s' khong co trong 'item_catalog'." % item)

    # -- 7.3 jumpscare -> item ----------------------------------------------
    for js_id, (area_id, js) in sorted(ch.jumpscares.items()):
        tii = js.get("trigger_item_id")
        if is_str(tii) and tii not in ch.items:
            broken += 1
            rep.error("%s / %s" % (area_id, js_id),
                      "trigger_item_id = '%s' khong co trong 'item_catalog'." % tii)

    # -- 7.4 manifest -> file area ------------------------------------------
    for area_id, uc in sorted(ch.unlock.items()):
        where = "chapter_01.json / %s" % area_id
        for item in uc["items"]:
            if item not in ch.items:
                broken += 1
                rep.error(where, "unlock_condition.required_items chua '%s' khong co trong "
                                 "'item_catalog'." % item)
        if uc["from"] is not None and uc["from"] not in ch.areas:
            broken += 1
            rep.error(where, "unlock_condition.from_area_id = '%s' khong ton tai." % uc["from"])
        if is_str(uc["entry"]) and uc["entry"] not in ch.hotspots:
            broken += 1
            rep.error(where, "unlock_condition.entry_hotspot_id = '%s' khong ton tai." % uc["entry"])

    # -- 7.5 item_catalog -> nguon san sinh ---------------------------------
    for item_id, meta in sorted(ch.items.items()):
        if not is_dict(meta):
            continue
        src = meta.get("nguon")
        if is_str(src) and src not in ch.hotspots and src not in ch.puzzles:
            broken += 1
            rep.error("chapter_01.json / item_catalog / %s" % item_id,
                      "Truong 'nguon' = '%s' khong tro toi hotspot hay puzzle nao co that."
                      % src)
        home = meta.get("nhat_o_area")
        if is_str(home) and home not in ch.areas:
            broken += 1
            rep.error("chapter_01.json / item_catalog / %s" % item_id,
                      "Truong 'nhat_o_area' = '%s' khong ton tai." % home)

    if not broken:
        rep.ok("Toan bo tham chieu cheo (target_puzzle_id, wrong_action_jumpscare, item_id, "
               "required_item, target_area_id) deu tro toi doi tuong co that.")


# --------------------------------------------------------------------------
# CO TIEN TRINH (FLAG) - xac dinh nguon cap
# --------------------------------------------------------------------------

def collect_flag_references(ch: Chapter):
    """flag_id -> danh sach noi THAM CHIEU toi co do (de bao loi co dia chi cu the)."""
    refs = defaultdict(list)
    for area_id, uc in sorted(ch.unlock.items()):
        for flag in uc["flags"]:
            if is_str(flag):
                refs[flag].append("chapter_01.json / %s / unlock_condition.required_flags"
                                  % area_id)
    for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
        for flag in str_list(hs, "required_flags"):
            refs[flag].append("%s / %s / required_flags" % (area_id, hs_id))
    return refs


def build_flag_producers(ch: Chapter, rep: Report) -> None:
    """
    Xac dinh nguon cap cho moi co tien trinh. CHI HAI NGUON, ca hai deu doc duoc bang may:

      1. TUONG MINH - truong "grants_flag" tren mot hotspot hoac mot puzzle.
      2. QUY UOC CHINH TAC - giai cau do X luon bat co "flag_<X>_solved". Day la mot luat
         suy dien CO DINH, khong phai phong doan: no khong phu thuoc vao cach dat ten cua
         ai ca, va engine hien thuc dung luat do.

    KHONG con muc "suy luan" thu ba. Truoc day trinh kiem doan nguon cap bang cach so tu
    khoa trung giua ten co va ten hotspot, roi GIAI DOAN 10 nap chinh cai doan do vao mo
    phong nguoi choi - nen mo phong "di duoc" bang nhung canh do chinh no bia ra, va bao
    cao ket luan "[OK] KHA GIAI 5/5 khu vuc" cho mot ban du lieu ma nguoi choi that chi
    di duoc 2/5. Phan suy luan nay bay gio chi con la GOI Y [i] cho nguoi thiet ke, in o
    cuoi giai doan, va khong ham nao doc lai no.

    Co duoc tham chieu (unlock_condition.required_flags / hotspot.required_flags) ma khong
    co nguon cap nao -> [LOI]. Khong phai [CANH BAO]: khu vuc doi co do khong bao gio mo.
    """
    producers = defaultdict(list)

    # -- muc 1: tuong minh ---------------------------------------------------
    for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
        gf = hs.get("grants_flag")
        if is_str(gf):
            producers[gf].append(("hotspot", hs_id, area_id, "tuong minh"))
    for pz_id, (area_id, pz) in sorted(ch.puzzles.items()):
        gf = pz.get("grants_flag")
        if is_str(gf):
            producers[gf].append(("puzzle", pz_id, area_id, "tuong minh"))
        # -- muc 2: quy uoc chinh tac
        producers["flag_%s_solved" % pz_id].append(("puzzle", pz_id, area_id, "quy uoc"))

    ch.flag_producers = dict(producers)

    # -- doi chieu voi cac co THUC SU duoc tham chieu ------------------------
    refs = collect_flag_references(ch)
    dangling = [flag for flag in sorted(refs) if not producers.get(flag)]

    for flag in dangling:
        rep.error(
            "co tien trinh '%s'" % flag,
            "KHONG co nguon cap: khong hotspot hay puzzle nao khai bao \"grants_flag\": "
            "\"%s\", va ten co cung khong khop quy uoc flag_<puzzle_id>_solved. Co nay "
            "khong bao gio bat len duoc, nen %d cho dang doi no se ket cung vinh vien: %s"
            % (flag, len(refs[flag]), fmt_list(refs[flag], limit=4)),
            "Them \"grants_flag\": \"%s\" vao dung hotspot (hoac puzzle) chiu trach nhiem bat "
            "co nay. Trinh kiem KHONG con doan nguon cap tu ten nua - viec bat co phai nam "
            "trong du lieu." % flag,
        )

    # -- co duoc cap nhung khong ai doi --------------------------------------
    #
    # Mot co khong ai doi TRONG CHUONG 1 chua chac la rac: no co the la co ban giao cho
    # chuong sau hoac cho lop luu game (vd flag_chapter_01_hoan_thanh). Trinh kiem khong
    # nhin thay nhung chuong do, va no tuyet doi khong duoc doan y dinh tu TEN co - do
    # dung la thoi quen da lam hong ban truoc. Cach dung dan: manifest khai bao tuong minh
    # danh sach 'exported_flags', va nhung co trong do khong bi nhac nua.
    exported = set(ch.exported_flags)
    for flag in sorted(exported):
        if not producers.get(flag):
            rep.error(
                "chapter_01.json / exported_flags",
                "Khai bao xuat co '%s' sang chuong sau, nhung KHONG cho nao trong Chuong 1 cap "
                "co nay - chuong sau se doi mai mot co khong bao gio den." % flag,
                "Them \"grants_flag\": \"%s\" vao hotspot/puzzle chiu trach nhiem, hoac bo ten "
                "nay khoi 'exported_flags'." % flag,
            )

    for flag, prods in sorted(producers.items()):
        if flag in refs or flag in exported:
            continue
        explicit = [p for p in prods if p[3] == "tuong minh"]
        if not explicit:
            continue        # co quy uoc khong ai dung la binh thuong
        rep.warn(
            "co tien trinh '%s'" % flag,
            "Duoc cap tuong minh boi %s nhung KHONG mot unlock_condition hay required_flags "
            "nao trong Chuong 1 doi toi. Hoac day la loi chinh ta o noi tham chieu, hoac la "
            "co thua, hoac la co ban giao sang chuong sau ma chua khai bao."
            % fmt_list("%s '%s'" % (p[0], p[1]) for p in explicit),
            "Neu la loi chinh ta: doi chieu voi cac required_flags trong chapter_01.json. "
            "Neu co that su thua: bo grants_flag. Neu co nay danh cho chuong sau / lop luu "
            "game: them \"%s\" vao mang \"exported_flags\" o cap cao nhat cua chapter_01.json "
            "- khai bao y do bang du lieu thi trinh kiem thoi nhac." % flag,
        )

    n_explicit = sum(1 for prods in producers.values() for p in prods if p[3] == "tuong minh")
    n_conv = sum(1 for prods in producers.values() for p in prods if p[3] == "quy uoc")
    rep.info("Nguon cap co tien trinh: %d khai bao TUONG MINH (grants_flag) + %d theo QUY UOC "
             "CHINH TAC (flag_<puzzle_id>_solved). Khong co nguon nao duoc suy luan."
             % (n_explicit, n_conv))

    if dangling:
        suggest_flag_sources(ch, dangling, rep)


def suggest_flag_sources(ch: Chapter, dangling, rep: Report) -> None:
    """
    GOI Y (chi de nguoi doc), khong phai ket luan.

    Doi chieu tu khoa giua ten co va ten hotspot USE_ITEM de doan xem designer CO LE dinh
    cho hotspot nao bat co. Ket qua chay thang ra man hinh duoi dang [i] va DUNG O DO:
    khong ham nao nap lai, dac biet la mo phong kha giai o GIAI DOAN 10. Day chinh la cho
    ban audit truoc bi thung - trinh kiem tu tin vao phong doan cua chinh no.
    """
    for flag in dangling:
        scope = None
        for area_id, uc in sorted(ch.unlock.items()):
            if flag in uc["flags"] and is_str(uc["from"]):
                scope = uc["from"]
                break

        flag_tokens = tokens_of(flag)
        candidates = []
        for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
            if hs.get("action_type") != "USE_ITEM":
                continue
            if is_str(hs.get("grants_flag")):
                continue        # hotspot nay da co co rieng roi
            overlap = flag_tokens & tokens_of(hs_id)
            if not overlap:
                continue
            score = len(overlap) + (1 if scope is not None and area_id == scope else 0)
            candidates.append((score, hs_id, area_id, sorted(overlap)))

        if not candidates:
            continue
        candidates.sort(reverse=True)
        lines = ", ".join("%s (%s; tu chung: %s)" % (hs_id, area_id, "/".join(ov))
                          for _, hs_id, area_id, ov in candidates[:3])
        rep.hint(
            "goi y nguon cap cho '%s'" % flag,
            "Doan tu ten (chi doi chieu tu khoa, KHONG phai bang chung): co the designer dinh "
            "cho mot trong cac hotspot USE_ITEM sau bat co nay - %s. Neu dung, hay them "
            "\"grants_flag\": \"%s\" vao dung mot trong so do." % (lines, flag),
        )


# --------------------------------------------------------------------------
# GIAI DOAN 8: DO THI PHU THUOC VAT PHAM + PHAT HIEN CHU TRINH
# --------------------------------------------------------------------------

def build_item_graph(ch: Chapter):
    """
    Dung do thi phu thuoc CUNG giua cac vat pham.

    Canh A -> B nghia la: "phai co A truoc thi moi lay duoc B", va dieu do dung voi
    MOI cach lay B. Chi lay giao cua cac tap dieu kien tren tat ca nguon san sinh B,
    nen mot chu trinh trong do thi nay la be tac that su, khong phai bao dong gia
    do con duong thay the.

    Tra ve (graph, producers) voi graph[A] = set(B).
    """
    producers = defaultdict(list)   # item_id -> list[set dieu kien]

    def area_prereq(area_id):
        uc = ch.unlock.get(area_id)
        if not uc or uc["type"] == "NONE":
            return set()
        return set(uc["items"])

    for hs_id, (area_id, hs) in ch.hotspots.items():
        action = hs.get("action_type")
        gained = hs.get("item_id")
        if not is_str(gained):
            continue
        if action == "COLLECT_ITEM":
            need = set()
            if is_str(hs.get("required_item")):
                need.add(hs["required_item"])
            producers[gained].append(need | area_prereq(area_id))
        elif action == "USE_ITEM":
            req = hs.get("required_item")
            if is_str(req) and req != gained:
                producers[gained].append({req} | area_prereq(area_id))

    for pz_id, (area_id, pz) in ch.puzzles.items():
        rid = pz.get("reward_item_id")
        if not is_str(rid):
            continue
        need = set(str_list(pz, "required_items"))
        producers[rid].append(need | area_prereq(area_id))

    graph = defaultdict(set)
    for item_id, prereq_sets in producers.items():
        if not prereq_sets:
            continue
        hard = set.intersection(*prereq_sets) if len(prereq_sets) > 1 else set(prereq_sets[0])
        for dep in hard:
            if dep != item_id:
                graph[dep].add(item_id)
    return graph, producers


def find_cycles(graph):
    """DFS lap (khong de quy, khong so tran stack) tim moi chu trinh trong do thi."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycles = []
    nodes = set(graph) | {v for vs in graph.values() for v in vs}

    for root in sorted(nodes):
        if color[root] != WHITE:
            continue
        stack = [(root, iter(sorted(graph.get(root, ()))))]
        path = [root]
        color[root] = GRAY
        while stack:
            node, children = stack[-1]
            advanced = False
            for nxt in children:
                if color[nxt] == GRAY:                     # quay lai mot dinh dang tham
                    cycles.append(path[path.index(nxt):] + [nxt])
                elif color[nxt] == WHITE:
                    color[nxt] = GRAY
                    path.append(nxt)
                    stack.append((nxt, iter(sorted(graph.get(nxt, ())))))
                    advanced = True
                    break
            if not advanced:
                color[node] = BLACK
                stack.pop()
                if path:
                    path.pop()
    return cycles


def check_item_cycles(ch: Chapter, rep: Report):
    graph, producers = build_item_graph(ch)
    cycles = find_cycles(graph)

    if cycles:
        seen = set()
        for cycle in cycles:
            key = frozenset(cycle)
            if key in seen:
                continue
            seen.add(key)
            rep.error(
                "do thi phu thuoc vat pham",
                "CHU TRINH: %s - moi vat pham trong vong nay deu doi mot vat pham khac "
                "cung vong, nen khong bao gio lay duoc cai nao." % " -> ".join(cycle),
                "Cat mot canh: bo 'required_item' o mot mat xich, hoac doi mot vat pham "
                "sang nhat o khu vuc truoc do.",
            )
    else:
        n_edges = sum(len(v) for v in graph.values())
        rep.ok("Do thi phu thuoc vat pham (%d dinh, %d canh cung) khong co chu trinh."
               % (len(ch.items), n_edges))

    orphan = [i for i in sorted(ch.items) if not producers.get(i)]
    for item_id in orphan:
        rep.error(
            "chapter_01.json / item_catalog / %s" % item_id,
            "Vat pham nay khong co nguon san sinh nao: khong hotspot COLLECT_ITEM nao trao no, "
            "cung khong puzzle nao lay no lam 'reward_item_id'.",
            "Them mot hotspot COLLECT_ITEM voi \"item_id\": \"%s\", hoac gan no lam phan "
            "thuong cua mot cau do." % item_id,
        )
    return graph, producers


# --------------------------------------------------------------------------
# GIAI DOAN 9: VAT PHAM "CHET"
# --------------------------------------------------------------------------

def check_dead_items(ch: Chapter, rep: Report) -> None:
    """Vat pham nhat duoc ma khong o dau doi toi -> canh bao (thuong la thiet ke bo sot)."""
    consumers = defaultdict(list)

    for hs_id, (area_id, hs) in ch.hotspots.items():
        req = hs.get("required_item")
        if is_str(req):
            consumers[req].append("hotspot %s (%s, %s)" % (hs_id, area_id, hs.get("action_type")))
    for pz_id, (area_id, pz) in ch.puzzles.items():
        for item in str_list(pz, "required_items"):
            consumers[item].append("puzzle %s (%s)" % (pz_id, area_id))
    for area_id, uc in ch.unlock.items():
        for item in uc["items"]:
            consumers[item].append("dieu kien mo khoa %s" % area_id)

    dead = [i for i in sorted(ch.items) if not consumers.get(i)]
    for item_id in dead:
        meta = ch.items.get(item_id) or {}
        purpose = meta.get("dung_de") or meta.get("mo_ta_vi") or ""
        hint = ("Ban mo ta cong dung la: \"%s\" - hay ma hoa cong dung do thanh du lieu: "
                % purpose.strip()[:150]) if purpose else ""
        rep.warn(
            "vat pham chet '%s'" % item_id,
            "Nhat duoc nhung KHONG o dau doi toi: khong hotspot nao dat no lam 'required_item', "
            "khong cau do nao liet ke no trong 'required_items', khong khu vuc nao can no de mo.",
            hint + "them \"required_items\": [\"%s\"] vao cau do dung no lam cong cu, hoac "
                   "them mot hotspot USE_ITEM voi \"required_item\": \"%s\"." % (item_id, item_id),
        )
    if not dead:
        rep.ok("Moi vat pham trong item_catalog deu co noi dung toi - khong co vat pham chet.")


def check_dead_jumpscares(ch: Chapter, rep: Report) -> None:
    """
    GIAI DOAN 9 - CU DOA CHET: cu doa nam trong du lieu nhung khong mot luot choi nao ban
    duoc no ra.

    Truong hop nang nhat, va la truong hop de lot nhat: jumpscare ON_COLLECT_ITEM tro toi
    mot vat pham ma nguoi choi KHONG BAO GIO "nhat" - vi du vat pham do chi la
    reward_item_id cua mot cau do (nguoi choi nhan no qua man hinh giai do, khong qua mot
    hotspot COLLECT_ITEM nao). Su kien ON_COLLECT_ITEM khong bao gio ban ra, va ca mot
    canh dinh cao cua chuong im lang - khong crash, khong log, khong ai biet.
    """
    # Vat pham thuc su duoc NHAT qua hotspot COLLECT_ITEM, kem khu vuc nhat duoc.
    collected_in = defaultdict(set)
    for hs_id, (area_id, hs) in ch.hotspots.items():
        if hs.get("action_type") == "COLLECT_ITEM" and is_str(hs.get("item_id")):
            collected_in[hs["item_id"]].add(area_id)

    # Vat pham chi den tu phan thuong cau do / hotspot USE_ITEM (KHONG phai "nhat").
    reward_of = {}
    for pz_id, (area_id, pz) in ch.puzzles.items():
        if is_str(pz.get("reward_item_id")):
            reward_of[pz["reward_item_id"]] = "phan thuong cua cau do '%s'" % pz_id
    for hs_id, (area_id, hs) in ch.hotspots.items():
        if hs.get("action_type") == "USE_ITEM" and is_str(hs.get("item_id")):
            reward_of.setdefault(hs["item_id"], "san pham cua hotspot USE_ITEM '%s'" % hs_id)

    dead = 0
    for js_id, (area_id, js) in sorted(ch.jumpscares.items()):
        where = "%s / %s" % (area_id, js_id)
        trig = js.get("trigger_type")

        if trig == "ON_COLLECT_ITEM":
            tii = js.get("trigger_item_id")
            if not is_str(tii):
                continue            # thieu truong - da bao o GIAI DOAN 2-3
            if tii not in ch.items:
                continue            # tham chieu gay - da bao o GIAI DOAN 7b
            if not collected_in.get(tii):
                dead += 1
                how = reward_of.get(tii)
                rep.error(
                    where,
                    "CU DOA CHET: trigger la ON_COLLECT_ITEM tren '%s', nhung vat pham do "
                    "KHONG BAO GIO duoc nhat qua mot hotspot COLLECT_ITEM nao - %s. Su kien "
                    "'vua nhat duoc vat pham' khong bao gio phat ra, nen cu doa nay khong the "
                    "ban trong bat ky luot choi nao."
                    % (tii, ("no chi la %s" % how) if how
                       else "khong co nguon nao trao no qua duong nhat do ca"),
                    "Chon mot trong ba: (a) doi 'trigger_item_id' sang mot vat pham co hotspot "
                    "COLLECT_ITEM that; (b) them mot hotspot COLLECT_ITEM trao '%s'; "
                    "(c) doi 'trigger_type' sang ON_PUZZLE_FAIL_COUNT / ON_ENTER_AREA cho khop "
                    "voi cach vat pham nay thuc su den tay nguoi choi." % tii,
                )
            elif area_id not in collected_in[tii]:
                rep.warn(
                    where,
                    "Cu doa ON_COLLECT_ITEM nay thuoc khu vuc '%s', nhung '%s' chi nhat duoc o "
                    "%s. Neu engine chi nap jumpscare cua khu vuc dang dung thi no se khong bao "
                    "gio ban." % (area_id, tii, fmt_list(sorted(collected_in[tii]))),
                    "Chuyen khai bao cu doa sang dung file area noi nhat duoc vat pham.",
                )

        elif trig == "ON_PUZZLE_FAIL_COUNT":
            users = [pz_id for pz_id, (_, pz) in ch.puzzles.items()
                     if pz.get("wrong_action_jumpscare") == js_id]
            if not users:
                rep.warn(
                    where,
                    "Cu doa ON_PUZZLE_FAIL_COUNT nay khong duoc cau do nao tro toi qua "
                    "'wrong_action_jumpscare' - khong co bo dem sai nao dem toi no, nen no "
                    "khong bao gio ban.",
                    "Dat \"wrong_action_jumpscare\": \"%s\" o cau do tuong ung, hoac xoa cu "
                    "doa neu da bo." % js_id,
                )

        elif trig == "ON_WRONG_ITEM_USE":
            tii = js.get("trigger_item_id")
            if is_str(tii) and tii in ch.items and not any(
                    h.get("required_item") == tii or h.get("item_id") == tii
                    for _, (_, h) in ch.hotspots.items()):
                rep.warn(
                    where,
                    "Cu doa ON_WRONG_ITEM_USE tro toi '%s' nhung khong hotspot nao dung toi vat "
                    "pham do - kha nang cao no khong bao gio ban." % tii,
                )

    if not dead:
        rep.ok("Khong co cu doa chet: moi jumpscare deu co duong kich hoat co that.")


# --------------------------------------------------------------------------
# GIAI DOAN 10: KHA GIAI - THUAT TOAN DIEM BAT DONG
# --------------------------------------------------------------------------

def simulate_player(ch: Chapter, rep: Report, trace_enabled: bool = False):
    """
    Mo phong nguoi choi bang thuat toan diem bat dong (fixpoint / least fixed point).

    NGUON DU KIEN - va CHI nhung nguon nay:
      * hotspot.required_item      vat pham phai co trong tui do
      * hotspot.required_flags     co tien trinh phai bat du (AND)
      * hotspot.grants_flag        co duoc bat khi hotspot chay xong  <- TUONG MINH
      * puzzle.required_items      dung cu phai cam moi nhap duoc loi giai
      * puzzle.grants_flag         co phu bat khi giai dung           <- TUONG MINH
      * quy uoc chinh tac          giai cau do X bat co flag_<X>_solved
      * unlock_condition           dieu kien vao khu vuc trong chapter_01.json

    Mo phong KHONG doc bang suy luan cua build_flag_producers. Ban truoc no co doc, va do
    la ly do trinh kiem in "[OK] KHA GIAI ... 5/5 khu vuc" trong khi mot mo phong doc lap
    chi di duoc 2/5: no tu cap cho minh nhung canh ma du lieu khong he co, roi di tren
    chinh nhung canh do. Mot ket luan nguy nguy hiem hon mot ket luan bo trong - nguoi ta
    dong bo len build vi tin no.

    Vong lap: moi vong quet toan bo hotspot cua nhung khu vuc DA toi duoc va lam moi viec
    lam duoc voi trang thai hien tai. Vong nao khong doi trang thai nua thi dung - do la
    diem bat dong, tuc toan bo phan nguoi choi co the voi toi.

    GIA DINH DUOC GHI RO: tui do KHONG bi tieu hao (dung vat pham xong van con giu). Day la
    gia dinh noi long; no co the bo qua mot be tac do vat pham bi an mat, nhung khong bao
    gio bia them duong di. Neu engine that su tieu hao vat pham, phai sua ham nay cho khop
    chu khong duoc de hai ben lech nhau.
    """
    reached = set()
    inventory = set()
    solved = set()
    flags = set()
    fired = set()
    trace = []

    def unlock_ok(area_id):
        uc = ch.unlock.get(area_id)
        if not uc or uc["type"] == "NONE":
            return True
        got_items = [i in inventory for i in uc["items"]]
        got_flags = [f in flags for f in uc["flags"]]
        checks = got_items + got_flags
        if not checks:
            return True
        return any(checks) if uc["type"] == "ANY_OF" else all(checks)

    def missing_for(area_id):
        uc = ch.unlock.get(area_id) or {"items": [], "flags": []}
        return ([i for i in uc["items"] if i not in inventory],
                [f for f in uc["flags"] if f not in flags])

    def grant_flag(flag, source, rnd):
        """Chi bat co khi du lieu NOI RO la co duoc bat. Khong co duong nao khac vao day."""
        if is_str(flag) and flag not in flags:
            flags.add(flag)
            trace.append((rnd, "CO", flag, source))

    def gate_missing(hs):
        """Thu con thieu de hotspot nay kha dung: (vat pham, co tien trinh)."""
        miss_items = []
        req = hs.get("required_item")
        if is_str(req) and req not in inventory:
            miss_items.append(req)
        miss_flags = [f for f in str_list(hs, "required_flags") if f not in flags]
        return miss_items, miss_flags

    start = ch.start_area_id or (ch.area_order[0] if ch.area_order else None)
    if not start:
        rep.error("kha giai", "Manifest khong chi ra khu vuc mo man ('start_area_id').")
        return None
    if start not in ch.areas:
        rep.error("kha giai", "Khu vuc mo man '%s' khong nap duoc - khong the mo phong." % start)
        return None
    if not unlock_ok(start):
        rep.error("kha giai", "Khu vuc mo man '%s' co dieu kien mo khoa khong the thoa man "
                              "luc bat dau - nguoi choi khong vao duoc game." % start)
        return None
    reached.add(start)
    trace.append((0, "KHU VUC", start, "mo man"))

    round_no = 0
    MAX_ROUNDS = 200
    while round_no < MAX_ROUNDS:
        round_no += 1
        changed = False

        for area_id in sorted(reached):
            for hs in ch.area_hotspots(area_id):
                hs_id = hs["id"]
                action = hs.get("action_type")

                if hs.get("enabled") is False:
                    continue

                # -- cong chan chung cho MOI loai hotspot --------------------
                miss_items, miss_flags = gate_missing(hs)
                if miss_items or miss_flags:
                    continue

                if action == "COLLECT_ITEM":
                    if hs_id in fired:
                        continue
                    item_id = hs.get("item_id")
                    fired.add(hs_id)
                    changed = True
                    if is_str(item_id) and item_id not in inventory:
                        inventory.add(item_id)
                        trace.append((round_no, "VAT PHAM", item_id,
                                      "nhat tai %s / %s" % (area_id, hs_id)))
                    grant_flag(hs.get("grants_flag"), "%s / %s" % (area_id, hs_id), round_no)

                elif action == "USE_ITEM":
                    if hs_id in fired:
                        continue
                    req = hs.get("required_item")
                    if not is_str(req):
                        continue        # du lieu hong - da bao [LOI] o GIAI DOAN 2-3
                    fired.add(hs_id)
                    changed = True
                    item_id = hs.get("item_id")
                    if is_str(item_id) and item_id != req and item_id not in inventory:
                        inventory.add(item_id)
                        trace.append((round_no, "VAT PHAM", item_id,
                                      "tao ra tai %s / %s" % (area_id, hs_id)))
                    grant_flag(hs.get("grants_flag"),
                               "%s / %s (dung %s)" % (area_id, hs_id, req), round_no)

                elif action == "ZOOM_PUZZLE":
                    pz_id = hs.get("target_puzzle_id")
                    if not is_str(pz_id) or pz_id in solved:
                        continue
                    entry = ch.puzzles.get(pz_id)
                    if not entry or entry[0] != area_id:
                        continue
                    pz = entry[1]
                    tools = str_list(pz, "required_items")
                    if any(t not in inventory for t in tools):
                        continue
                    solved.add(pz_id)
                    changed = True
                    trace.append((round_no, "CAU DO", pz_id, "giai tai %s" % area_id))
                    grant_flag("flag_%s_solved" % pz_id, "giai %s (quy uoc)" % pz_id, round_no)
                    grant_flag(pz.get("grants_flag"), "giai %s (grants_flag)" % pz_id, round_no)
                    grant_flag(hs.get("grants_flag"), "%s / %s" % (area_id, hs_id), round_no)
                    rid = pz.get("reward_item_id")
                    if is_str(rid) and rid not in inventory:
                        inventory.add(rid)
                        trace.append((round_no, "VAT PHAM", rid, "phan thuong cua %s" % pz_id))

                elif action == "CHANGE_AREA":
                    target = hs.get("target_area_id")
                    if not is_str(target) or target not in ch.areas:
                        continue
                    if hs_id not in fired:
                        fired.add(hs_id)
                        changed = True
                        grant_flag(hs.get("grants_flag"), "%s / %s" % (area_id, hs_id), round_no)
                    if target in reached or not unlock_ok(target):
                        continue
                    reached.add(target)
                    changed = True
                    trace.append((round_no, "KHU VUC", target,
                                  "di tu %s / %s" % (area_id, hs_id)))

                else:   # EXAMINE / DIALOGUE - chi dang ke khi co bat co
                    if hs_id in fired or not is_str(hs.get("grants_flag")):
                        continue
                    fired.add(hs_id)
                    changed = True
                    grant_flag(hs["grants_flag"], "%s / %s" % (area_id, hs_id), round_no)

        if not changed:
            break

    result = {
        "reached": reached, "inventory": inventory, "solved": solved,
        "flags": flags, "rounds": round_no, "trace": trace,
    }

    # ---- doi chieu diem bat dong voi muc tieu ------------------------------
    failed = False

    unreached = [a for a in ch.area_order if a not in reached]
    for area_id in unreached:
        failed = True
        miss_items, miss_flags = missing_for(area_id)
        detail = []
        if miss_items:
            detail.append("thieu vat pham: %s" % fmt_list(miss_items))
        if miss_flags:
            detail.append("thieu co tien trinh: %s" % fmt_list(miss_flags))
        if not detail:
            doors = [h for h, (a, hsx) in ch.hotspots.items()
                     if hsx.get("action_type") == "CHANGE_AREA"
                     and hsx.get("target_area_id") == area_id]
            open_doors = [d for d in doors if ch.hotspots[d][0] in reached]
            if not doors:
                detail.append("khong co hotspot CHANGE_AREA nao tro toi khu vuc nay")
            elif not open_doors:
                detail.append("chi co loi vao tu khu vuc chua toi duoc: %s"
                              % fmt_list("%s (o %s)" % (d, ch.hotspots[d][0]) for d in doors))
            else:
                blocked_doors = []
                for d in open_doors:
                    mi, mf = gate_missing(ch.hotspots[d][1])
                    blocked_doors.append("%s can %s" % (d, fmt_list(mi + mf) if (mi or mf)
                                                        else "(khong ro)"))
                detail.append("loi vao bi chan: %s" % fmt_list(blocked_doors))
        rep.error(
            "kha giai / %s" % area_id,
            "KHONG toi duoc khu vuc nay du da vet can moi duong (%d vong lap). %s"
            % (round_no, "; ".join(detail)),
            "Doi chieu unlock_condition cua khu vuc trong chapter_01.json voi nhung gi nguoi "
            "choi thuc su cam duoc truoc do.",
        )

    final_area = ch.final_area_id()
    if final_area and final_area not in reached:
        failed = True
        rep.error("kha giai / khu vuc cuoi",
                  "Khong toi duoc khu vuc ket chuong '%s' - Chuong 1 khong the hoan thanh."
                  % final_area)

    for pz_id, (area_id, pz) in sorted(ch.puzzles.items()):
        if pz_id in solved:
            continue
        failed = True
        tools = [i for i in str_list(pz, "required_items") if i not in inventory]
        openers = [h for h in ch.area_hotspots(area_id)
                   if h.get("action_type") == "ZOOM_PUZZLE"
                   and h.get("target_puzzle_id") == pz_id]
        if area_id not in reached:
            why = "khu vuc '%s' khong toi duoc" % area_id
        elif not openers:
            why = "khong co hotspot ZOOM_PUZZLE nao trong '%s' mo duoc no" % area_id
        elif tools:
            why = "thieu vat pham cong cu: %s" % fmt_list(tools)
        else:
            blockers = []
            for h in openers:
                mi, mf = gate_missing(h)
                if mi or mf:
                    blockers.append("%s can %s" % (h["id"], fmt_list(mi + mf)))
            why = ("hotspot mo no bi chan: %s" % fmt_list(blockers)) if blockers \
                else "khong xac dinh duoc - kiem tra lai du lieu khu vuc"
        rep.error("kha giai / %s" % pz_id,
                  "Cau do khong bao gio giai duoc: %s." % why,
                  "Neu day la cau do tuy chon, hay ghi chu ro; neu bat buoc, mo duong den no.")

    for item_id in sorted(ch.items):
        if item_id in inventory:
            continue
        failed = True
        sources = []
        for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
            if hs.get("item_id") == item_id:
                mi, mf = gate_missing(hs)
                sources.append("%s (%s)%s" % (hs_id, area_id,
                                              "" if area_id in reached
                                              else " - khu vuc chua toi duoc"
                                              if not (mi or mf) else
                                              " - can %s" % fmt_list(mi + mf)))
        for pz_id, (area_id, pz) in sorted(ch.puzzles.items()):
            if pz.get("reward_item_id") == item_id:
                sources.append("phan thuong cua %s (%s)%s"
                               % (pz_id, area_id, "" if pz_id in solved else " - chua giai duoc"))
        rep.error("kha giai / %s" % item_id,
                  "Vat pham khong bao gio cam duoc - nguoi choi hoan thanh chuong ma khong "
                  "the so vao no. Nguon duy nhat: %s" % fmt_list(sources),
                  "Kiem tra khu vuc chua no co toi duoc khong, va dieu kien 'required_item' / "
                  "'required_flags' cua hotspot trao no co thoa man duoc khong.")

    reward_items = {pz.get("reward_item_id") for _, pz in ch.puzzles.values()
                    if is_str(pz.get("reward_item_id"))}
    missing_rewards = sorted(r for r in reward_items if r not in inventory)
    if missing_rewards:
        failed = True
        rep.error("kha giai / phan thuong",
                  "Khong lay duoc phan thuong cua cau do: %s." % fmt_list(missing_rewards))

    # ---- KET DUNG O DAU: in nguyen trang thai diem bat dong ----------------
    if failed:
        report_stop_point(ch, rep, result, gate_missing)
    else:
        rep.ok("KHA GIAI: dat diem bat dong sau %d vong lap, CHI dung nguon cap tuong minh. "
               "Nguoi choi di duoc tu '%s' toi khu vuc ket chuong '%s'."
               % (round_no, start, final_area))
        rep.plain("Toi duoc %d/%d khu vuc  |  giai %d/%d cau do  |  cam %d/%d vat pham  |  "
                  "bat %d co tien trinh."
                  % (len(reached), len(ch.area_order), len(solved), len(ch.puzzles),
                     len(inventory), len(ch.items), len(flags)))
        rep.plain("Gia dinh cua mo phong: tui do khong bi tieu hao; khong mot co tien trinh nao "
                  "duoc suy luan - tat ca den tu grants_flag hoac quy uoc flag_<puzzle_id>_solved.")

    if trace_enabled:
        rep.info("Nhat ky mo phong nguoi choi (thu tu thuc te game mo ra):")
        for rnd, kind, target, how in trace:
            rep.plain("  vong %-2d  %-9s %-28s %s" % (rnd, kind, target, how))

    return result


def report_stop_point(ch: Chapter, rep: Report, result, gate_missing) -> None:
    """
    In ro NGUOI CHOI KET DUNG O DAU va CON THIEU GI - phan quan trong nhat cua mot bao cao
    that bai. Bao "khong kha giai" ma khong noi dung o dau thi nguoi sua phai do lai tu dau.
    """
    reached = result["reached"]
    inventory = result["inventory"]
    solved = result["solved"]
    flags = result["flags"]

    rep.plain("")
    rep.plain("KET DUNG O DAU - trang thai cuoi cung cua mo phong (sau %d vong lap):"
              % result["rounds"])
    rep.plain("  Khu vuc toi duoc (%d/%d): %s"
              % (len(reached), len(ch.area_order),
                 fmt_list([a for a in ch.area_order if a in reached], limit=12)))
    rep.plain("  Khu vuc KHONG toi duoc: %s"
              % fmt_list([a for a in ch.area_order if a not in reached], limit=12))
    rep.plain("  Vat pham cam duoc (%d/%d): %s"
              % (len(inventory), len(ch.items), fmt_list(sorted(inventory), limit=12)))
    rep.plain("  Vat pham CON THIEU: %s"
              % fmt_list(sorted(i for i in ch.items if i not in inventory), limit=12))
    rep.plain("  Cau do giai duoc (%d/%d): %s"
              % (len(solved), len(ch.puzzles), fmt_list(sorted(solved), limit=12)))
    rep.plain("  Cau do CON LAI: %s"
              % fmt_list(sorted(p for p in ch.puzzles if p not in solved), limit=12))
    rep.plain("  Co tien trinh bat duoc: %s" % fmt_list(sorted(flags), limit=12))

    needed_flags = sorted(set(collect_flag_references(ch)) - flags)
    if needed_flags:
        rep.plain("  Co tien trinh CON THIEU (co cho doi, khong bao gio bat): %s"
                  % fmt_list(needed_flags, limit=12))

    stuck = []
    for area_id in sorted(reached):
        for hs in ch.area_hotspots(area_id):
            if hs.get("enabled") is False:
                continue
            miss_items, miss_flags = gate_missing(hs)
            if not (miss_items or miss_flags):
                continue
            need = []
            if miss_items:
                need.append("vat pham %s" % fmt_list(miss_items))
            if miss_flags:
                need.append("co %s" % fmt_list(miss_flags))
            stuck.append("    %s / %s (%s) dang cho: %s"
                         % (area_id, hs["id"], hs.get("action_type"), "; ".join(need)))
    if stuck:
        rep.plain("  Hotspot trong tam tay nhung bi chan (%d):" % len(stuck))
        for line in stuck[:15]:
            rep.plain(line)
        if len(stuck) > 15:
            rep.plain("    ... va %d hotspot khac" % (len(stuck) - 15))
    else:
        rep.plain("  Khong hotspot nao trong vung voi toi con bi chan - be tac nam o "
                  "unlock_condition cua khu vuc, hoac khong con hotspot nao de lam.")
    rep.plain("")


# --------------------------------------------------------------------------
# GIAI DOAN 11: LIVEOPS
# --------------------------------------------------------------------------

def check_liveops(cfg, ch: Chapter, rep: Report) -> None:
    """Hien thuc cac bat bien liet ke o khoa 'validation.invariants' cua chinh file cau hinh."""
    if not is_dict(cfg):
        rep.error("liveops", "File cau hinh LiveOps phai la mot doi tuong JSON o cap cao nhat.")
        return

    W = "liveops_chapter_01.json"

    for key in ("schema_version", "config_id", "config_version", "chapter_id", "rollout",
                "hint_system", "iap", "seasonal_events", "gem_economy", "ad_placements",
                "telemetry", "remote_config_keys", "ab_tests", "player_safety_compliance"):
        if key not in cfg:
            rep.error(W, "Thieu khoi bat buoc '%s'." % key)

    if ch.chapter_id and cfg.get("chapter_id") != ch.chapter_id:
        rep.error(W, "chapter_id = '%s' khong khop voi manifest man choi ('%s')."
                  % (cfg.get("chapter_id"), ch.chapter_id))

    # ---- 1-4: he goi y -----------------------------------------------------
    hint = cfg.get("hint_system")
    if is_dict(hint):
        for mf in ("hint_cost_gems", "ads_reward_hints"):
            if not is_int(hint.get(mf)):
                rep.error(W, "Khoa Master Form 'hint_system.%s' thieu hoac khong phai so nguyen."
                          % mf)

        tiers = hint.get("tiers")
        if is_list(tiers) and tiers:
            ordered = sorted((t for t in tiers if is_dict(t)), key=lambda t: t.get("tier", 0))
            costs = [t.get("gem_cost") for t in ordered]
            waits = [t.get("unlock_free_after_sec") for t in ordered]

            if all(is_int(c) for c in costs) and any(costs[i] > costs[i + 1] for i in range(len(costs) - 1)):
                rep.error(W, "BAT BIEN 1 vo hieu: hint_system.tiers[*].gem_cost phai tang dan "
                             "theo tier, dang la %s." % costs,
                          "Tier cao hon phai dat hon hoac bang tier thap hon.")
            if all(is_int(s) for s in waits) and any(waits[i] > waits[i + 1] for i in range(len(waits) - 1)):
                rep.error(W, "BAT BIEN 2 vo hieu: hint_system.tiers[*].unlock_free_after_sec "
                             "phai tang dan theo tier, dang la %s." % waits)

            cap = hint.get("max_wait_sec_to_full_solution")
            if is_int(cap) and waits and is_int(waits[-1]) and waits[-1] > cap:
                rep.error(W, "BAT BIEN 3 vo hieu: tier cuoi mo mien phi sau %d giay, vuot tran "
                             "max_wait_sec_to_full_solution = %d giay." % (waits[-1], cap),
                          "Nguyen tac N1 bao dam nguoi choi luon co duong mien phi trong %d giay."
                          % cap)
        else:
            rep.error(W, "hint_system.tiers phai la mang khong rong.")

        if hint.get("free_path_guaranteed") is not True:
            rep.error(W, "BAT BIEN 4 vo hieu: hint_system.free_path_guaranteed phai la true "
                         "(nguyen tac N1 - Chuong 1 choi tron ven khong ton mot dong).")
        sources = hint.get("unlock_sources")
        if is_list(sources):
            free = [s for s in sources if is_dict(s)
                    and s.get("gem_cost") == 0 and s.get("ads_required") == 0]
            if not free:
                rep.error(W, "BAT BIEN 4 vo hieu: khong co unlock_source nao mien phi hoan toan "
                             "(gem_cost = 0 VA ads_required = 0).")

        # tham chieu cheo sang du lieu man choi
        for i, ov in enumerate(hint.get("per_puzzle_overrides") or []):
            if not is_dict(ov):
                continue
            where = "%s / hint_system.per_puzzle_overrides[%d]" % (W, i)
            pid, aid = ov.get("puzzle_id"), ov.get("area_id")
            if is_str(pid) and ch.puzzles and pid not in ch.puzzles:
                rep.error(where, "puzzle_id = '%s' khong ton tai trong data/areas/." % pid)
            elif is_str(pid) and pid in ch.puzzles and is_str(aid) and ch.puzzles[pid][0] != aid:
                rep.error(where, "puzzle_id '%s' thuc te nam o khu vuc '%s', khong phai '%s'."
                          % (pid, ch.puzzles[pid][0], aid))
            if is_str(aid) and ch.areas and aid not in ch.areas:
                rep.error(where, "area_id = '%s' khong ton tai." % aid)

        if ch.puzzles:
            covered = {ov.get("puzzle_id") for ov in (hint.get("per_puzzle_overrides") or [])
                       if is_dict(ov)}
            missing = sorted(p for p in ch.puzzles if p not in covered)
            if missing:
                rep.warn(W, "Cac cau do chua co muc trong hint_system.per_puzzle_overrides: %s"
                         % fmt_list(missing),
                         "Cau do khong co muc rieng se dung moc thoi gian mac dinh, co the "
                         "qua som hoac qua muon so voi do kho that.")

        btn = hint.get("hint_button")
        if is_dict(btn) and is_dict(btn.get("bounds")):
            check_bounds(btn["bounds"], rep, "%s / hint_system.hint_button" % W)

    # ---- 5-6: IAP ----------------------------------------------------------
    iap = cfg.get("iap")
    if is_dict(iap):
        products = iap.get("products") or []
        seen_pid = defaultdict(int)
        for i, prod in enumerate(products):
            if not is_dict(prod):
                continue
            where = "%s / iap.products[%d]" % (W, i)
            pid = prod.get("iap_product_id")
            if not is_str(pid):
                rep.error(where, "Thieu khoa Master Form 'iap_product_id'.")
            else:
                seen_pid[pid] += 1
            if not is_num(prod.get("price_usd")) or prod.get("price_usd") <= 0:
                rep.error(where, "Khoa Master Form 'price_usd' thieu hoac khong phai so duong.")

            regions = prod.get("regional_pricing") or []
            codes = [r.get("region_code") for r in regions if is_dict(r)]
            dup = sorted({c for c in codes if codes.count(c) > 1})
            if dup:
                rep.error(where, "BAT BIEN 6 vo hieu: region_code trung trong cung san pham: %s"
                          % fmt_list(dup))
            for need in ("VN", "US", "SEA_DEFAULT"):
                if need not in codes:
                    rep.error(where, "BAT BIEN 6 vo hieu: thieu vung gia bat buoc '%s'." % need,
                              "Ba vung neo VN / US / SEA_DEFAULT phai co mat o moi san pham.")

        for pid, n in sorted(seen_pid.items()):
            if n > 1:
                rep.error(W, "BAT BIEN 5 vo hieu: iap_product_id '%s' khai bao %d lan." % (pid, n))

        paywall = iap.get("paywall")
        if is_dict(paywall):
            never = paywall.get("never_show_during") or []
            for need in ("JUMPSCARE_ENVELOPE", "PUZZLE", "CUTSCENE"):
                if need not in never:
                    rep.error(W, "iap.paywall.never_show_during thieu '%s' - vi pham nguyen tac "
                                 "N3 (khong kiem tien tren noi so)." % need)
            if paywall.get("dismissible") is not True:
                rep.error(W, "iap.paywall.dismissible phai la true - khong duoc nhot nguoi choi "
                             "trong man mua hang.")

        fair = iap.get("fair_play")
        if is_dict(fair):
            allowed = {"CONTENT_UNLOCK", "CONVENIENCE_HINT", "COSMETIC"}
            extra = [c for c in (fair.get("sellable_categories") or []) if c not in allowed]
            if extra:
                rep.error(W, "BAT BIEN N2 vo hieu: sellable_categories chua hang muc ngoai tap "
                             "cho phep: %s" % fmt_list(extra))
            if fair.get("no_pay_to_win") is not True:
                rep.error(W, "iap.fair_play.no_pay_to_win phai la true.")

    # ---- 7-10: su kien theo mua -------------------------------------------
    events = cfg.get("seasonal_events") or []
    windows = []
    for i, evt in enumerate(events):
        if not is_dict(evt):
            continue
        where = "%s / seasonal_events[%d]" % (W, i)
        start, end = evt.get("event_start"), evt.get("event_end")

        if not is_str(start) or not RE_ISO_DATE.match(start):
            rep.error(where, "Khoa Master Form 'event_start' thieu hoac sai dinh dang YYYY-MM-DD.")
        if not is_str(end) or not RE_ISO_DATE.match(end):
            rep.error(where, "'event_end' thieu hoac sai dinh dang YYYY-MM-DD.")
        if is_str(start) and is_str(end) and RE_ISO_DATE.match(start) and RE_ISO_DATE.match(end):
            if start >= end:
                rep.error(where, "BAT BIEN 7 vo hieu: event_start (%s) phai truoc event_end (%s)."
                          % (start, end))
            else:
                areas_hit = [a for a in (evt.get("applies_to_areas") or []) if is_str(a)]
                if evt.get("enabled") is True:
                    windows.append((start, end, set(areas_hit), evt.get("event_id", "?"), where))

        bg = evt.get("override_bg")
        if not is_str(bg):
            rep.error(where, "Thieu khoa Master Form 'override_bg'.")
        else:
            bundles = ((evt.get("addressables") or {}).get("bundles")
                       if is_dict(evt.get("addressables")) else None) or []
            if bg not in bundles:
                rep.error(where, "BAT BIEN 9 vo hieu: override_bg = '%s' khong nam trong "
                                 "addressables.bundles %s." % (bg, fmt_list(bundles)),
                          "May se doi mot bundle khong bao gio duoc tai ve - nen se roi vao "
                          "nhanh fallback mai mai.")

        for area_id in (evt.get("applies_to_areas") or []):
            if is_str(area_id) and ch.areas and area_id not in ch.areas:
                rep.error(where, "applies_to_areas chua '%s' khong ton tai trong chapter manifest."
                          % area_id)

        theme = evt.get("theme_override")
        if is_dict(theme):
            frozen = theme.get("does_not_change") or []
            for need in ("hotspot_bounds", "puzzle_solution", "jumpscare_trigger_type", "max_fails"):
                if need not in frozen:
                    rep.error(where, "BAT BIEN 10 vo hieu: theme_override.does_not_change thieu "
                                     "'%s'." % need,
                              "Su kien theo mua chi duoc doi lop trang tri, khong duoc cham vao "
                              "phan cot loi cua man choi.")

        fb = evt.get("fallback")
        if is_dict(fb) and fb.get("never_block_gameplay") is not True:
            rep.error(where, "fallback.never_block_gameplay phai la true - tai giao dien su kien "
                             "that bai khong duoc chan nguoi choi.")
        elif not is_dict(fb):
            rep.error(where, "Thieu khoi 'fallback' - phai co duong lui khi tai bundle that bai.")

    for i in range(len(windows)):
        for j in range(i + 1, len(windows)):
            s1, e1, a1, id1, w1 = windows[i]
            s2, e2, a2, id2, _ = windows[j]
            shared = a1 & a2
            if shared and s1 < e2 and s2 < e1:
                rep.error(w1, "BAT BIEN 8 vo hieu: su kien '%s' (%s..%s) va '%s' (%s..%s) cung "
                              "bat va chong cua so thoi gian tren khu vuc %s - khong doan duoc "
                              "giao dien nao thang." % (id1, s1, e1, id2, s2, e2, fmt_list(shared)),
                          "Tach cua so thoi gian, hoac dung 'priority' va tat bot mot su kien.")

    # ---- 11: quang cao -----------------------------------------------------
    for i, ad in enumerate(cfg.get("ad_placements") or []):
        if not is_dict(ad):
            continue
        where = "%s / ad_placements[%d]" % (W, i)
        blocked = ad.get("blocked_windows") or []
        for need in ("DURING_JUMPSCARE_ENVELOPE", "WITHIN_90S_AFTER_ANY_JUMPSCARE"):
            if need not in blocked:
                rep.error(where, "BAT BIEN 11 vo hieu: blocked_windows thieu '%s'." % need,
                          "Nguyen tac N3 - khong kiem tien tren noi so. Cua so nay bat buoc.")
        if ad.get("opt_in_only") is not True:
            rep.error(where, "opt_in_only phai la true - chi quang cao thuong co chu dich.")
        if ad.get("ad_format") not in ("REWARDED_VIDEO", "REWARDED_INTERSTITIAL"):
            rep.error(where, "ad_format = '%s' bi cam trong Chuong 1 - chi cho phep quang cao "
                             "thuong." % ad.get("ad_format"))

    # ---- 12: khong hop qua ngau nhien -------------------------------------
    safety = cfg.get("player_safety_compliance")
    if is_dict(safety):
        loot = safety.get("no_loot_box")
        if is_dict(loot):
            if loot.get("randomized_paid_rewards") is not False:
                rep.error(W, "BAT BIEN 12 vo hieu: no_loot_box.randomized_paid_rewards phai la "
                             "false - khong gacha, khong quay so, khong hop qua ngau nhien.")
            if loot.get("randomized_product_ids"):
                rep.error(W, "BAT BIEN 12 vo hieu: randomized_product_ids phai rong.")
        else:
            rep.error(W, "Thieu khoi 'player_safety_compliance.no_loot_box'.")

        acc = safety.get("accessibility_never_monetized")
        if is_dict(acc):
            # CHI xet cac khoa CO GIA TRI BOOLEAN. Khoi nay chua ca ghi chu san xuat bang
            # tieng Viet ("mo_ta_vi", "ghi_chu_vi", "validator_rule") - do la CHUOI, khong
            # phai co an toan. Ban truoc doi MOI khoa === true nen mot dong ghi chu bi bao
            # [LOI] oan; ma vi do la [LOI] duy nhat, no lam ca trinh kiem that bai va day
            # nhung loi chet chuong that su xuong hang [CANH BAO] phia sau. Thu tu uu tien
            # bi dao nguoc hoan toan: bao cao het bao dong gia, con loi that thi lot.
            NOTE_KEYS = ("mo_ta_vi", "ghi_chu_vi", "validator_rule")

            off = sorted(k for k, v in acc.items() if is_bool(v) and v is not True)
            if off:
                rep.error(W, "Nguyen tac N4 vo hieu: accessibility_never_monetized co co dat "
                             "false: %s" % fmt_list(off),
                          "Moi tuy chon an toan / tro nang phai mien phi va khong khoa sau moc "
                          "tien trinh - dat lai true.")

            odd = sorted(k for k, v in acc.items()
                         if not is_bool(v) and not (is_str(v) and k in NOTE_KEYS))
            if odd:
                rep.error(W, "accessibility_never_monetized co khoa khong doc duoc thanh co an "
                             "toan: %s. Khoi nay chi chap nhan gia tri boolean, cong ba khoa "
                             "ghi chu kieu chuoi (%s)."
                          % (fmt_list("%s=%r" % (k, acc[k]) for k in odd), ", ".join(NOTE_KEYS)),
                          "Doi gia tri ve true/false, hoac doi ten khoa ghi chu thanh "
                          "'mo_ta_vi'.")

            if not any(is_bool(v) for v in acc.values()):
                rep.error(W, "accessibility_never_monetized khong co MOT co boolean nao - "
                             "khoi nay dang rong ve mat logic, bat bien N4 khong duoc bao ve "
                             "boi gi ca.",
                          "Khai bao ro cac co, vd \"gentle_mode_free\": true, "
                          "\"photosensitive_safe_free\": true.")

    # ---- 13: telemetry -----------------------------------------------------
    tele = cfg.get("telemetry")
    if is_dict(tele):
        names = defaultdict(int)
        for i, evt in enumerate(tele.get("events") or []):
            if not is_dict(evt):
                continue
            where = "%s / telemetry.events[%d]" % (W, i)
            name = evt.get("event_name")
            if not is_str(name):
                rep.error(where, "Thieu 'event_name'.")
                continue
            names[name] += 1
            if not RE_SNAKE.match(name):
                rep.error(where, "BAT BIEN 13 vo hieu: event_name '%s' khong phai snake_case "
                                 "thuan." % name)
            if len(name) > 40:
                rep.error(where, "BAT BIEN 13 vo hieu: event_name '%s' dai %d ky tu, vuot tran 40."
                          % (name, len(name)))
            params = evt.get("params") or []
            if len(params) > 25:
                rep.error(where, "Su kien '%s' co %d tham so, vuot tran 25 cua Firebase."
                          % (name, len(params)))
        for name, n in sorted(names.items()):
            if n > 1:
                rep.error(W, "BAT BIEN 13 vo hieu: event_name '%s' trung %d lan." % (name, n))

    # ---- 14-15: A/B test + remote config ----------------------------------
    rc_keys = set()
    for i, entry in enumerate(cfg.get("remote_config_keys") or []):
        if not is_dict(entry):
            continue
        key = entry.get("key")
        if not is_str(key):
            rep.error("%s / remote_config_keys[%d]" % (W, i), "Thieu truong 'key'.")
            continue
        if key in rc_keys:
            rep.error(W, "BAT BIEN 15 vo hieu: remote_config_keys co khoa trung '%s'." % key)
        rc_keys.add(key)
        if entry.get("type") not in ("string", "int", "float", "bool", "json"):
            rep.error("%s / remote_config_keys[%d]" % (W, i),
                      "Truong 'type' = %r khong hop le." % (entry.get("type"),))

    ab = cfg.get("ab_tests")
    if is_dict(ab):
        for i, slot in enumerate(ab.get("slots") or []):
            if not is_dict(slot):
                continue
            where = "%s / ab_tests.slots[%d]" % (W, i)
            slot_id = slot.get("slot_id", "?")
            variants = [v for v in (slot.get("variants") or []) if is_dict(v)]
            total = sum(v.get("allocation_pct", 0) for v in variants
                        if is_num(v.get("allocation_pct")))
            if abs(total - 100) > 1e-6:
                rep.error(where, "BAT BIEN 14 vo hieu: tong allocation_pct cua slot '%s' bang %g, "
                                 "phai bang 100." % (slot_id, total),
                          "Chia lai ty le giua cac nhanh cho du 100.")
            seen_variant = set()
            for v in variants:
                vid = v.get("variant_id")
                if vid in seen_variant:
                    rep.error(where, "variant_id '%s' trung trong slot '%s'." % (vid, slot_id))
                seen_variant.add(vid)
                for key in (v.get("overrides") or {}):
                    if rc_keys and key not in rc_keys:
                        rep.error(where, "BAT BIEN 15 vo hieu: nhanh '%s' ghi de khoa '%s' khong "
                                         "co trong remote_config_keys." % (vid, key),
                                  "Khai bao '%s' trong remote_config_keys, neu khong may se "
                                  "khong bao gio doc duoc gia tri ghi de nay." % key)

    # ---- 16: kinh te gem ---------------------------------------------------
    gem = cfg.get("gem_economy")
    if is_dict(gem):
        bt = gem.get("balance_targets")
        if is_dict(bt):
            earn = bt.get("expected_free_earn_chapter_01")
            spend = bt.get("expected_spend_p90_player")
            if is_int(earn) and is_int(spend) and earn < spend:
                rep.error(W, "BAT BIEN 16 vo hieu: nguoi choi mien phi kiem duoc %d gem nhung "
                             "muc chi p90 la %d gem - nhom p90 se bi ep tra tien." % (earn, spend),
                          "Tang nguon gem mien phi hoac giam gia goi y.")
            if bt.get("free_player_can_finish_without_gems") is not True:
                rep.error(W, "free_player_can_finish_without_gems phai la true (nguyen tac N1).")
        sink_ids, src_ids = set(), set()
        for s in (gem.get("sources") or []):
            if is_dict(s) and is_str(s.get("source_id")):
                if s["source_id"] in src_ids:
                    rep.error(W, "gem_economy.sources co source_id trung '%s'." % s["source_id"])
                src_ids.add(s["source_id"])
        for s in (gem.get("sinks") or []):
            if is_dict(s) and is_str(s.get("sink_id")):
                if s["sink_id"] in sink_ids:
                    rep.error(W, "gem_economy.sinks co sink_id trung '%s'." % s["sink_id"])
                sink_ids.add(s["sink_id"])

    # ---- doi chieu khoa Master Form ---------------------------------------
    mf_checks = [
        ("hint_cost_gems", is_dict(hint) and is_int(hint.get("hint_cost_gems"))),
        ("ads_reward_hints", is_dict(hint) and is_int(hint.get("ads_reward_hints"))),
        ("iap_product_id", is_dict(iap) and bool(iap.get("products"))
            and is_dict(iap["products"][0]) and is_str(iap["products"][0].get("iap_product_id"))),
        ("price_usd", is_dict(iap) and bool(iap.get("products"))
            and is_dict(iap["products"][0]) and is_num(iap["products"][0].get("price_usd"))),
        ("event_start", bool(events) and is_dict(events[0]) and is_str(events[0].get("event_start"))),
        ("override_bg", bool(events) and is_dict(events[0]) and is_str(events[0].get("override_bg"))),
    ]
    missing_mf = [name for name, ok in mf_checks if not ok]
    if missing_mf:
        rep.error(W, "Thieu khoa Master Form bat buoc: %s" % fmt_list(missing_mf),
                  "Sau khoa nay khong duoc doi ten hay doi vi tri.")
    else:
        rep.ok("Du sau khoa Master Form: hint_cost_gems, ads_reward_hints, iap_product_id, "
               "price_usd, event_start, override_bg.")

    invariants = ((cfg.get("validation") or {}).get("invariants")
                  if is_dict(cfg.get("validation")) else None)
    if is_list(invariants):
        rep.info("File cau hinh tu khai bao %d bat bien; trinh kiem nay hien thuc toan bo 16 "
                 "bat bien goc." % len(invariants))


# --------------------------------------------------------------------------
# DIEU PHOI
# --------------------------------------------------------------------------

def run(args) -> int:
    use_color = sys.stdout.isatty() and not args.no_color and not os.environ.get("NO_COLOR")
    palette = Palette(use_color)
    rep = Report(palette, quiet=args.quiet, strict=args.strict)

    data_dir = os.path.abspath(args.data_dir)
    manifest_path = args.manifest or os.path.join(data_dir, "chapter_01.json")
    areas_dir = os.path.join(data_dir, "areas")

    ch = Chapter()

    # ---- GIAI DOAN 1: doc du lieu -----------------------------------------
    rep.section("GIAI DOAN 1 - DOC & PHAN TICH JSON")
    manifest = load_json(manifest_path, rep, "chapter_01.json")
    if manifest is None:
        rep.render("KIEM CHUNG DU LIEU MAN CHOI - LINH AN THON CHAPTER 1")
        return rep.render_summary(args.strict)
    rep.ok("Doc duoc manifest chuong: %s" % manifest_path)

    if not is_dict(manifest):
        rep.error("chapter_01.json", "Manifest phai la mot doi tuong JSON o cap cao nhat.")
        rep.render("KIEM CHUNG DU LIEU MAN CHOI - LINH AN THON CHAPTER 1")
        return rep.render_summary(args.strict)

    ch.chapter_id = manifest.get("chapter_id")
    ch.start_area_id = manifest.get("start_area_id")
    ch.area_order = [a for a in (manifest.get("area_order") or []) if is_str(a)]

    # 'exported_flags' (tuy chon): co tien trinh Chuong 1 bat len de ban giao cho chuong
    # sau hoac cho lop luu game. Khai bao o day de trinh kiem khong coi chung la co thua.
    raw_exported = manifest.get("exported_flags")
    if raw_exported is not None and not is_list(raw_exported):
        rep.error("chapter_01.json", "'exported_flags' phai la mang flag_id (co the bo trong).")
    else:
        for flag in (raw_exported or []):
            if not is_str(flag) or not flag.startswith(PREFIX["flag"]):
                rep.error("chapter_01.json / exported_flags",
                          "Gia tri khong hop le: %r - phai la chuoi bat dau bang '%s'."
                          % (flag, PREFIX["flag"]))
            else:
                ch.exported_flags.append(flag)

    if not is_str(ch.chapter_id):
        rep.error("chapter_01.json", "Thieu truong bat buoc 'chapter_id'.")
    if not ch.area_order:
        rep.error("chapter_01.json", "Thieu 'area_order' - khong biet thu tu khu vuc trong chuong.")

    for entry in (manifest.get("item_catalog") or []):
        if is_dict(entry) and is_str(entry.get("item_id")):
            item_id = entry["item_id"]
            if item_id in ch.items:
                rep.error("chapter_01.json / item_catalog",
                          "item_id '%s' khai bao nhieu lan." % item_id)
            if not item_id.startswith(PREFIX["item"]):
                rep.error("chapter_01.json / item_catalog",
                          "item_id '%s' phai bat dau bang '%s'." % (item_id, PREFIX["item"]))
            ch.items[item_id] = entry

    manifest_areas = {}
    for entry in (manifest.get("areas") or []):
        if is_dict(entry) and is_str(entry.get("area_id")):
            manifest_areas[entry["area_id"]] = entry

    for area_id in ch.area_order:
        if not area_id.startswith(PREFIX["area"]):
            rep.error("chapter_01.json / area_order",
                      "area_id '%s' phai bat dau bang '%s'." % (area_id, PREFIX["area"]))
        entry = manifest_areas.get(area_id)
        rel = (entry or {}).get("file") or os.path.join("areas", area_id + ".json")
        path = os.path.join(data_dir, rel) if not os.path.isabs(rel) else rel
        area = load_json(path, rep, "%s (%s)" % (area_id, rel))
        if area is None:
            continue
        if not is_dict(area):
            rep.error(area_id, "File area phai la mot doi tuong JSON o cap cao nhat.")
            continue
        ch.areas[area_id] = area
        ch.unlock[area_id] = normalize_unlock((entry or {}).get("unlock_condition"), area_id, rep)

    for area_id in sorted(manifest_areas):
        if area_id not in ch.area_order:
            rep.error("chapter_01.json", "Khu vuc '%s' khai bao trong 'areas' nhung khong co "
                                         "trong 'area_order' - se khong bao gio duoc nap." % area_id)

    if os.path.isdir(areas_dir):
        for name in sorted(os.listdir(areas_dir)):
            if not name.endswith(".json"):
                continue
            stem = name[:-5]
            if stem not in ch.areas:
                rep.warn("areas/%s" % name,
                         "File khu vuc nay khong duoc manifest tham chieu - se khong bao gio "
                         "duoc nap, va khong duoc kiem.",
                         "Them '%s' vao 'area_order' va 'areas' cua chapter_01.json, hoac xoa "
                         "file neu da bo." % stem)

    if ch.areas:
        rep.ok("Doc duoc %d/%d file khu vuc." % (len(ch.areas), len(ch.area_order)))

    # ---- GIAI DOAN 2-4: cau truc + rang buoc co dieu kien + hinh hoc -------
    rep.section("GIAI DOAN 2-4 - CAU TRUC, RANG BUOC THEO LOAI, HINH HOC 1920x1080")
    for area_id in ch.area_order:
        area = ch.areas.get(area_id)
        if area is None:
            continue
        if area.get("chapter_id") != ch.chapter_id:
            rep.error(area_id, "chapter_id trong file ('%s') khong khop manifest ('%s')."
                      % (area.get("chapter_id"), ch.chapter_id))
        if area.get("area_id") != area_id:
            rep.error(area_id, "area_id trong file ('%s') khong khop ten file / manifest ('%s')."
                      % (area.get("area_id"), area_id))

        bg = area.get("background_asset_url")
        if not is_str(bg):
            rep.error(area_id, "Thieu truong bat buoc 'background_asset_url'.")
        elif not RE_BUNDLE_URL.match(bg):
            rep.error(area_id, "background_asset_url = '%s' phai la URL HTTPS tro toi mot file "
                               ".bundle." % bg,
                      "Toan bo asset di qua Addressables remote - khong nhung anh vao APK engine.")

        hotspots = area.get("hotspots")
        if not is_list(hotspots) or not hotspots:
            rep.error(area_id, "'hotspots' phai la mang khong rong - khu vuc khong co vung cham "
                               "la ngo cut.")
            hotspots = []
        for idx, hs in enumerate(hotspots):
            if check_hotspot(hs, rep, area_id, idx) and is_str(hs.get("id")):
                ch.hotspots[hs["id"]] = (area_id, hs)

        puzzles = area.get("puzzles")
        if not is_list(puzzles):
            rep.error(area_id, "'puzzles' phai la mang (co the rong).")
            puzzles = []
        for idx, pz in enumerate(puzzles):
            if check_puzzle(pz, rep, area_id, idx) and is_str(pz.get("id")):
                ch.puzzles[pz["id"]] = (area_id, pz)

        jumpscares = area.get("jumpscares")
        if not is_list(jumpscares):
            rep.error(area_id, "'jumpscares' phai la mang (co the rong).")
            jumpscares = []
        for idx, js in enumerate(jumpscares):
            if check_jumpscare(js, rep, area_id, idx) and is_str(js.get("id")):
                ch.jumpscares[js["id"]] = (area_id, js)

    if ch.areas and not rep.errors:
        rep.ok("Moi hotspot / puzzle / jumpscare deu du truong bat buoc, dung enum va nam tron "
               "trong khung %dx%d." % (DESIGN_WIDTH, DESIGN_HEIGHT))

    # ---- GIAI DOAN 5: chong lan -------------------------------------------
    rep.section("GIAI DOAN 5 - HOTSPOT CHONG LAN TRONG CUNG KHU VUC")
    for area_id in ch.area_order:
        area = ch.areas.get(area_id)
        if area and is_list(area.get("hotspots")):
            check_overlaps(area_id, area["hotspots"], rep)

    # ---- GIAI DOAN 6: id duy nhat -----------------------------------------
    rep.section("GIAI DOAN 6 - DINH DANH DUY NHAT TOAN CHUONG")
    check_duplicate_within_files(ch.areas, rep)
    check_unique_ids(ch, rep)

    # ---- co tien trinh -----------------------------------------------------
    rep.section("GIAI DOAN 7a - NGUON CAP CO TIEN TRINH (CHI TUONG MINH)")
    build_flag_producers(ch, rep)
    if ch.flag_producers:
        rep.ok("Xac dinh duoc nguon cap cho %d co tien trinh." % len(ch.flag_producers))

    # ---- GIAI DOAN 7: tham chieu cheo -------------------------------------
    rep.section("GIAI DOAN 7b - THAM CHIEU CHEO")
    check_cross_references(ch, rep)

    # ---- GIAI DOAN 8: chu trinh -------------------------------------------
    rep.section("GIAI DOAN 8 - CHU TRINH TRONG DO THI PHU THUOC VAT PHAM")
    check_item_cycles(ch, rep)

    # ---- GIAI DOAN 9: vat pham chet ---------------------------------------
    rep.section("GIAI DOAN 9 - VAT PHAM CHET / CU DOA CHET")
    check_dead_items(ch, rep)
    check_dead_jumpscares(ch, rep)

    # ---- GIAI DOAN 10: kha giai -------------------------------------------
    rep.section("GIAI DOAN 10 - KHA GIAI (MO PHONG DIEM BAT DONG)")
    if ch.areas:
        simulate_player(ch, rep, trace_enabled=args.trace)
    else:
        rep.error("kha giai", "Khong nap duoc khu vuc nao - bo qua buoc chung minh kha giai.")

    # ---- GIAI DOAN 11: liveops --------------------------------------------
    if not args.skip_liveops:
        rep.section("GIAI DOAN 11 - LIVEOPS & MONETIZATION")
        liveops_path = args.liveops or os.path.join(data_dir, "liveops_chapter_01.json")
        if not os.path.isfile(liveops_path) and not args.liveops:
            rep.warn("liveops_chapter_01.json",
                     "Khong tim thay file cau hinh LiveOps tai %s - bo qua giai doan 11."
                     % liveops_path)
        else:
            cfg = load_json(liveops_path, rep, "liveops_chapter_01.json")
            if cfg is not None:
                rep.ok("Doc duoc cau hinh LiveOps: %s" % liveops_path)
                check_liveops(cfg, ch, rep)

    rep.render("KIEM CHUNG DU LIEU MAN CHOI - LINH AN THON CHAPTER 1")
    return rep.render_summary(args.strict)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate_level.py",
        description="Kiem chung du lieu man choi Linh An Thon - Chapter 1 "
                    "(chi dung thu vien chuan Python 3).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ma thoat: 0 = sach, 1 = co loi (hoac co canh bao khi chay voi --strict).",
    )
    parser.add_argument(
        "data_dir", nargs="?", default=DEFAULT_DATA_DIR,
        help="Duong dan thu muc data (mac dinh: %s)" % DEFAULT_DATA_DIR,
    )
    parser.add_argument("-m", "--manifest", default=None,
                        help="Duong dan manifest chuong (mac dinh: <data_dir>/chapter_01.json)")
    parser.add_argument("--liveops", default=None,
                        help="Duong dan file cau hinh LiveOps "
                             "(mac dinh: <data_dir>/liveops_chapter_01.json)")
    parser.add_argument("--skip-liveops", action="store_true",
                        help="Bo qua giai doan 11 (chi kiem du lieu man choi)")
    parser.add_argument("--strict", action="store_true",
                        help="NANG moi [CANH BAO] thanh [LOI] ngay tren ban in va trong ma "
                             "thoat - dung cho cong CI truoc khi khoa ban")
    parser.add_argument("--trace", action="store_true",
                        help="In nhat ky mo phong nguoi choi cua buoc chung minh kha giai")
    parser.add_argument("--no-color", action="store_true", help="Tat mau ANSI")
    parser.add_argument("--quiet", action="store_true",
                        help="Chi in cac muc co [LOI] hoac [CANH BAO]")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except KeyboardInterrupt:
        print("\nDa dung theo yeu cau nguoi dung.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
