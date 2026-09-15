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
  GIAI DOAN 3  Rang buoc co dieu kien theo action_type / trigger_type / puzzle type
  GIAI DOAN 4  Hinh hoc: bounds trong 1920x1080, width/height > 0, nguong cham 88x88
  GIAI DOAN 5  Hotspot chong lan trong cung mot khu vuc
  GIAI DOAN 6  Dinh danh duy nhat toan chuong + quy uoc tien to
  GIAI DOAN 7  Tham chieu cheo: target_puzzle_id, wrong_action_jumpscare, item_id,
               required_item, target_area_id deu tro toi doi tuong CO THAT
  GIAI DOAN 8  Do thi phu thuoc vat pham: phat hien CHU TRINH (deadlock thiet ke)
  GIAI DOAN 9  Vat pham "chet": nhat duoc ma khong bao gio dung toi
  GIAI DOAN 10 KHA GIAI: mo phong nguoi choi bang thuat toan diem bat dong (fixpoint)
  GIAI DOAN 11 LiveOps: cac bat bien trong data/liveops_chapter_01.json

Ma thoat: 0 = sach (co the con [CANH BAO]), 1 = co it nhat mot [LOI].
Voi --strict thi [CANH BAO] cung lam ma thoat = 1.

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
MIN_TOUCH_SIZE = 88          # nguong cham ngon tay, duoi muc nay chi la CANH BAO

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
    """Gom ket qua kiem tra theo tung giai doan roi in mot lan, co mau."""

    def __init__(self, palette: Palette, quiet: bool = False) -> None:
        self.p = palette
        self.quiet = quiet
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
        self.warnings.append((where, message))
        line = "  %s %s\n      %s" % (self.p.yellow("[CANH BAO]"), self.p.bold(where), message)
        if fix:
            line += "\n      %s %s" % (self.p.dim("Cach sua:"), self.p.dim(fix))
        self._push(line)

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
        if n_err:
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

def check_bounds(bounds, rep: Report, where: str) -> bool:
    """GIAI DOAN 4. Tra ve True neu bounds hop le ve kieu du lieu."""
    if not is_dict(bounds):
        rep.error(where, "Truong 'bounds' phai la doi tuong {x, y, width, height}.")
        return False

    ok_types = True
    for key in ("x", "y", "width", "height"):
        if key not in bounds:
            rep.error(where, "Truong 'bounds' thieu khoa bat buoc '%s'." % key)
            ok_types = False
        elif not is_int(bounds[key]):
            rep.error(where, "bounds.%s phai la so nguyen, dang nhan '%r'." % (key, bounds[key]))
            ok_types = False
    if not ok_types:
        return False

    x, y = bounds["x"], bounds["y"]
    w, h = bounds["width"], bounds["height"]

    if w <= 0:
        rep.error(where, "bounds.width = %d - phai lon hon 0." % w)
    if h <= 0:
        rep.error(where, "bounds.height = %d - phai lon hon 0." % h)
    if x < 0 or y < 0:
        rep.error(where, "bounds co toa do am (x=%d, y=%d). Goc (0,0) o GOC TREN-BEN TRAI." % (x, y))

    if w > 0 and h > 0:
        if x + w > DESIGN_WIDTH:
            rep.error(
                where,
                "Vung cham tran mep phai: x + width = %d > %d." % (x + w, DESIGN_WIDTH),
                "Giam width xuong %d hoac keo x ve %d." % (DESIGN_WIDTH - x, DESIGN_WIDTH - w),
            )
        if y + h > DESIGN_HEIGHT:
            rep.error(
                where,
                "Vung cham tran mep duoi: y + height = %d > %d." % (y + h, DESIGN_HEIGHT),
                "Giam height xuong %d hoac keo y ve %d." % (DESIGN_HEIGHT - y, DESIGN_HEIGHT - h),
            )
        if w < MIN_TOUCH_SIZE or h < MIN_TOUCH_SIZE:
            rep.warn(
                where,
                "Vung cham %dx%d nho hon nguong ngon tay %dx%d - kho bam tren dien thoai."
                % (w, h, MIN_TOUCH_SIZE, MIN_TOUCH_SIZE),
                "No rong vung cham (bounds) ma khong can sua anh nen, hoac gop voi hotspot ben canh.",
            )
    return True


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
        check_bounds(hs["bounds"], rep, where)

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
        if not is_str(hs.get("item_id")) and not is_str(hs.get("target_puzzle_id")):
            rep.error(where, "USE_ITEM bat buoc co 'item_id' (trao vat pham moi) "
                             "HOAC 'target_puzzle_id' (mo cau do).")

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
    if is_str(gf) and not gf.startswith(PREFIX["flag"]):
        rep.error(where, "grants_flag = '%s' phai bat dau bang tien to '%s'."
                  % (gf, PREFIX["flag"]))
    return True


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

    if trig == "ON_TIMER":
        if "delay_sec" not in js:
            rep.warn(where, "ON_TIMER khong khai bao 'delay_sec' - thoi diem ban cu doa "
                            "khong xac dinh, moi may se ban mot kieu.",
                     "Them \"delay_sec\": <so giay dung yen trong khu vuc truoc khi ban>.")
        elif not is_num(js["delay_sec"]) or js["delay_sec"] <= 0:
            rep.error(where, "'delay_sec' phai la so duong.")
    elif "delay_sec" in js:
        rep.error(where, "Chi ON_TIMER moi duoc mang 'delay_sec'.")

    if trig not in ("ON_COLLECT_ITEM", "ON_WRONG_ITEM_USE") and "trigger_item_id" in js:
        rep.error(where, "Chi ON_COLLECT_ITEM / ON_WRONG_ITEM_USE moi duoc mang "
                         "'trigger_item_id'.")

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
        self.flag_producers = {}  # flag_id -> list[(kind, id, area_id)]

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

    items = [v for v in (raw.get("required_items") or []) if is_str(v)]
    flags = [v for v in (raw.get("required_flags") or []) if is_str(v)]
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

        for flag in (hs.get("required_flags") or []):
            if is_str(flag) and flag not in ch.flag_producers:
                broken += 1
                rep.error(where, "required_flags chua co '%s' khong co nguon cap nao." % flag)


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

        for item in (pz.get("required_items") or []):
            if is_str(item) and item not in ch.items:
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

def build_flag_producers(ch: Chapter, rep: Report) -> None:
    """
    Tim nguon cap cho moi co tien trinh, theo ba muc uu tien:

      1. TUONG MINH  - hotspot/puzzle co truong "grants_flag".
      2. QUY UOC     - flag_<puzzle_id>_solved duoc cap khi giai puzzle do.
      3. SUY LUAN    - doi chieu tu khoa giua ten co va id hotspot USE_ITEM trong
                       khu vuc nguon (from_area_id). Chi chap nhan khi ket qua
                       duy nhat, va luon kem mot [CANH BAO].

    Khong tim duoc nguon nao -> [LOI], vi khu vuc doi co do se khong bao gio mo.
    """
    producers = defaultdict(list)

    # muc 1 - tuong minh
    for hs_id, (area_id, hs) in ch.hotspots.items():
        gf = hs.get("grants_flag")
        if is_str(gf):
            producers[gf].append(("hotspot", hs_id, area_id, "tuong minh"))
    for pz_id, (area_id, pz) in ch.puzzles.items():
        gf = pz.get("grants_flag")
        if is_str(gf):
            producers[gf].append(("puzzle", pz_id, area_id, "tuong minh"))
        # muc 2 - quy uoc
        producers["flag_%s_solved" % pz_id].append(("puzzle", pz_id, area_id, "quy uoc"))

    # muc 3 - suy luan cho cac co duoc yeu cau nhung chua co nguon
    required_flags = set()
    for uc in ch.unlock.values():
        required_flags.update(uc["flags"])
    for _, (_, hs) in ch.hotspots.items():
        required_flags.update(f for f in (hs.get("required_flags") or []) if is_str(f))

    for flag in sorted(required_flags):
        if producers.get(flag):
            continue

        scope = None
        for area_id, uc in ch.unlock.items():
            if flag in uc["flags"] and is_str(uc["from"]):
                scope = uc["from"]
                break

        flag_tokens = tokens_of(flag)
        candidates = []
        for hs_id, (area_id, hs) in ch.hotspots.items():
            if hs.get("action_type") != "USE_ITEM":
                continue
            if scope is not None and area_id != scope:
                continue
            overlap = flag_tokens & tokens_of(hs_id)
            if overlap:
                candidates.append((len(overlap), hs_id, area_id, overlap))

        if not candidates:
            rep.error(
                "co tien trinh '%s'" % flag,
                "Khong tim duoc nguon cap co nay. Khu vuc doi no se khong bao gio mo duoc.",
                "Them \"grants_flag\": \"%s\" vao hotspot (hoac puzzle) chiu trach nhiem bat co."
                % flag,
            )
            continue

        candidates.sort(reverse=True)
        best = candidates[0][0]
        winners = [c for c in candidates if c[0] == best]
        if len(winners) > 1:
            rep.error(
                "co tien trinh '%s'" % flag,
                "Suy luan nguon cap ra %d ung vien ngang diem: %s - khong the ket luan."
                % (len(winners), fmt_list(w[1] for w in winners)),
                "Khai bao tuong minh \"grants_flag\": \"%s\" tren dung mot hotspot." % flag,
            )
            continue

        _, hs_id, area_id, overlap = winners[0]
        producers[flag].append(("hotspot", hs_id, area_id, "suy luan"))
        rep.warn(
            "co tien trinh '%s'" % flag,
            "Khong co truong 'grants_flag' nao cap co nay. Trinh kiem suy luan tu khoa chung "
            "%s va gan tam cho hotspot '%s' (%s)." % (fmt_list(sorted(overlap)), hs_id, area_id),
            "Them \"grants_flag\": \"%s\" vao hotspot '%s' de logic mo khoa doc duoc bang may, "
            "khong phu thuoc vao cach dat ten." % (flag, hs_id),
        )

    ch.flag_producers = dict(producers)


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
        need = {i for i in (pz.get("required_items") or []) if is_str(i)}
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
        for item in (pz.get("required_items") or []):
            if is_str(item):
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


# --------------------------------------------------------------------------
# GIAI DOAN 10: KHA GIAI - THUAT TOAN DIEM BAT DONG
# --------------------------------------------------------------------------

def simulate_player(ch: Chapter, rep: Report, trace_enabled: bool = False):
    """
    Mo phong nguoi choi bang thuat toan diem bat dong (fixpoint / least fixed point).

    Bat dau tu khu vuc mo man voi tui do rong, roi lap di lap lai: moi vong quet
    toan bo hotspot cua nhung khu vuc DA toi duoc va thu lam MOI viec lam duoc voi
    trang thai hien tai - nhat vat pham, dung vat pham, giai cau do, doi khu vuc.
    Vong nao khong lam trang thai thay doi nua thi dung: do la diem bat dong, tuc
    la toan bo phan nguoi choi co the voi toi.

    Sau do doi chieu diem bat dong voi muc tieu: toi duoc moi khu vuc, giai duoc moi
    cau do, cam duoc moi vat pham, va dac biet la toi duoc KHU VUC CUOI cung.
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
        if is_str(flag) and flag not in flags:
            flags.add(flag)
            trace.append((rnd, "CO", flag, source))

    # Suy luan nguoc: hotspot nao duoc gan lam nguon cap co (muc 3 o build_flag_producers).
    inferred = {}
    for flag, prods in ch.flag_producers.items():
        for kind, pid, area_id, how in prods:
            if kind == "hotspot" and how in ("suy luan", "tuong minh"):
                inferred.setdefault(pid, set()).add(flag)

    start = ch.start_area_id or (ch.area_order[0] if ch.area_order else None)
    if not start:
        rep.error("kha giai", "Manifest khong chi ra khu vuc mo man ('start_area_id').")
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

                need_flags = [f for f in (hs.get("required_flags") or []) if is_str(f)]
                if any(f not in flags for f in need_flags):
                    continue

                if action == "COLLECT_ITEM":
                    if hs_id in fired:
                        continue
                    req = hs.get("required_item")
                    if req is not None and req not in inventory:
                        continue
                    item_id = hs.get("item_id")
                    fired.add(hs_id)
                    changed = True
                    if is_str(item_id) and item_id not in inventory:
                        inventory.add(item_id)
                        trace.append((round_no, "VAT PHAM", item_id, "nhat tai %s / %s" % (area_id, hs_id)))
                    for flag in inferred.get(hs_id, ()):
                        grant_flag(flag, "%s / %s" % (area_id, hs_id), round_no)

                elif action == "USE_ITEM":
                    if hs_id in fired:
                        continue
                    req = hs.get("required_item")
                    if not is_str(req) or req not in inventory:
                        continue
                    fired.add(hs_id)
                    changed = True
                    item_id = hs.get("item_id")
                    if is_str(item_id) and item_id != req and item_id not in inventory:
                        inventory.add(item_id)
                        trace.append((round_no, "VAT PHAM", item_id, "tao ra tai %s / %s" % (area_id, hs_id)))
                    for flag in inferred.get(hs_id, ()):
                        grant_flag(flag, "%s / %s (dung %s)" % (area_id, hs_id, req), round_no)

                elif action == "ZOOM_PUZZLE":
                    pz_id = hs.get("target_puzzle_id")
                    if not is_str(pz_id) or pz_id in solved:
                        continue
                    entry = ch.puzzles.get(pz_id)
                    if not entry or entry[0] != area_id:
                        continue
                    pz = entry[1]
                    tools = [i for i in (pz.get("required_items") or []) if is_str(i)]
                    if any(t not in inventory for t in tools):
                        continue
                    solved.add(pz_id)
                    changed = True
                    trace.append((round_no, "CAU DO", pz_id, "giai tai %s" % area_id))
                    grant_flag("flag_%s_solved" % pz_id, "giai %s" % pz_id, round_no)
                    grant_flag(pz.get("grants_flag"), "giai %s" % pz_id, round_no)
                    rid = pz.get("reward_item_id")
                    if is_str(rid) and rid not in inventory:
                        inventory.add(rid)
                        trace.append((round_no, "VAT PHAM", rid, "phan thuong cua %s" % pz_id))

                elif action == "CHANGE_AREA":
                    target = hs.get("target_area_id")
                    if not is_str(target) or target in reached or target not in ch.areas:
                        continue
                    if unlock_ok(target):
                        reached.add(target)
                        changed = True
                        trace.append((round_no, "KHU VUC", target, "di tu %s / %s" % (area_id, hs_id)))

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
            detail.append("khong co loi vao nao kha dung"
                          if not doors
                          else "chi co loi vao tu khu vuc chua toi duoc: %s"
                               % fmt_list(ch.hotspots[d][0] for d in doors))
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
        tools = [i for i in (pz.get("required_items") or []) if is_str(i) and i not in inventory]
        if area_id not in reached:
            why = "khu vuc '%s' khong toi duoc" % area_id
        elif tools:
            why = "thieu vat pham cong cu: %s" % fmt_list(tools)
        elif not any(h.get("action_type") == "ZOOM_PUZZLE" and h.get("target_puzzle_id") == pz_id
                     for h in ch.area_hotspots(area_id)):
            why = "khong co hotspot ZOOM_PUZZLE nao mo duoc no"
        else:
            why = "hotspot mo no bi chan boi required_flags chua bat"
        rep.error("kha giai / %s" % pz_id,
                  "Cau do khong bao gio giai duoc: %s." % why,
                  "Neu day la cau do tuy chon, hay ghi chu ro; neu bat buoc, mo duong den no.")

    for item_id in sorted(ch.items):
        if item_id in inventory:
            continue
        failed = True
        rep.error("kha giai / %s" % item_id,
                  "Vat pham khong bao gio cam duoc - nguoi choi hoan thanh chuong ma khong "
                  "the so vao no.",
                  "Kiem tra khu vuc chua no co toi duoc khong, va dieu kien 'required_item' "
                  "cua hotspot trao no co thoa man duoc khong.")

    reward_items = {pz.get("reward_item_id") for _, pz in ch.puzzles.values()
                    if is_str(pz.get("reward_item_id"))}
    missing_rewards = sorted(r for r in reward_items if r not in inventory)
    if missing_rewards:
        failed = True
        rep.error("kha giai / phan thuong",
                  "Khong lay duoc phan thuong cua cau do: %s." % fmt_list(missing_rewards))

    if not failed:
        rep.ok("KHA GIAI: dat diem bat dong sau %d vong lap. Nguoi choi di duoc tu '%s' toi "
               "khu vuc ket chuong '%s'." % (round_no, start, final_area))
        rep.plain("Toi duoc %d/%d khu vuc  |  giai %d/%d cau do  |  cam %d/%d vat pham  |  "
                  "bat %d co tien trinh."
                  % (len(reached), len(ch.area_order), len(solved), len(ch.puzzles),
                     len(inventory), len(ch.items), len(flags)))

    if trace_enabled:
        rep.info("Nhat ky mo phong nguoi choi (thu tu thuc te game mo ra):")
        for rnd, kind, target, how in trace:
            rep.plain("  vong %-2d  %-9s %-28s %s" % (rnd, kind, target, how))

    return result


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
            bad = sorted(k for k, v in acc.items() if v is not True)
            if bad:
                rep.error(W, "Nguyen tac N4 vo hieu: accessibility_never_monetized co khoa khong "
                             "bang true: %s" % fmt_list(bad),
                          "Moi tuy chon an toan / tro nang phai mien phi va khong khoa sau moc "
                          "tien trinh.")

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
    rep = Report(palette, quiet=args.quiet)

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
    rep.section("GIAI DOAN 7a - NGUON CAP CO TIEN TRINH (FLAG)")
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
    rep.section("GIAI DOAN 9 - VAT PHAM CHET")
    check_dead_items(ch, rep)

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
                        help="Coi [CANH BAO] la loi - dung cho cong CI truoc khi khoa ban")
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
