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
  GIAI DOAN 4  Hinh hoc: bounds trong 1920x1080, width/height > 0, NGUONG CHAM CHINH THUC
               120 px @1920 (duoi 88 px la vi pham nang), visual_bounds nam tron trong bounds
  GIAI DOAN 5  Hotspot chong lan trong cung mot khu vuc
  GIAI DOAN 6  Dinh danh duy nhat toan chuong + quy uoc tien to
  GIAI DOAN 7  Nguon cap co tien trinh (CHI doc tu truong grants_flag) + tham chieu cheo
               + DOI CHIEU GUONG (7c): moi gia tri ma manifest LAP LAI tu file khu vuc
               (puzzle_index, jumpscare_index, flag_registry, background_asset_url,
               area_files) phai trung khop gia tri THAT trong data/areas/*.json
  GIAI DOAN 8  Do thi phu thuoc vat pham: phat hien CHU TRINH (deadlock thiet ke)
  GIAI DOAN 9  Vat pham "chet" + ngu nghia TIEU HAO vat pham (consumes_item / locks_item)
               + CU DOA CHET (jumpscare khong bao gio ban duoc)
  GIAI DOAN 10 KHA GIAI: mo phong nguoi choi bang thuat toan diem bat dong (fixpoint)
  GIAI DOAN 11 LiveOps: cac bat bien trong data/liveops_chapter_01.json

QUY TAC VANG CUA GIAI DOAN 10 - phien ban da go sach canh ao:
  Mo phong kha giai chi duoc nap nhung gi doc duoc tu GIA TRI cua cac truong trong JSON:
  grants_flag, required_flags, required_item, required_items, consumes_item, locks_item,
  unlock_condition. KHONG con luat suy dien nao ca.

  Hai vong truoc, trinh nay tu tay cap co bang cong thuc "flag_%s_solved" % puzzle_id va
  goi do la "quy uoc chinh tac". Cai ten nghe nhu mot hop dong, nhung chuoi ay dung tu
  TEN DINH DANH cua cau do chu khong tu bat ky truong nao trong du lieu - nen khi mot
  auditor xoa grants_flag cua puz_tuan_tu_le_cung (nguon cap tuong minh DUY NHAT cua
  flag_puz_tuan_tu_le_cung_solved), trinh kiem van in "[OK] KHA GIAI ... 5/5 khu vuc" va
  "DAT - du lieu sach hoan toan", thoat 0; trong khi mot mo phong doc lap chi di duoc
  3/5 khu vuc, 4/6 cau do va khong bao gio bat duoc co ket chuong. Canh ao da bi go bo
  hoan toan. Bu lai, puzzles[].grants_flag la truong BAT BUOC.

  Ngu nghia TIEU HAO VAT PHAM cung vay: mo phong khong con tu chon gia dinh "tui do khong
  bi tieu hao" nua, no doc truong consumes_item (va locks_item) cua tung hotspot USE_ITEM.

CHE DO TU KIEM DOT BIEN (--self-test):
  HAI TOAN TU dot bien, cham diem TACH RIENG:
    DOI GIA TRI  doi gia tri cua mot khoa dang co mat -> ban sao lech
    XOA KHOA     xoa han mot khoa                     -> ban sao khuyet
  Ba ho dot bien, chay noi tiep:
    (A) [XOA KHOA] Lan luot XOA tung truong grants_flag (moi puzzle, moi hotspot co khai
        bao) trong data/areas/* ngay trong bo nho, chay lai toan bo phep kiem, va doi
        trinh kiem PHAI bao loi o lop logic (GIAI DOAN 7a hoac 10).
    (B1) [DOI GIA TRI] Lan luot SUA tung gia tri ma manifest LAP LAI tu file khu vuc
        (puzzle_index, jumpscare_index, flag_registry, areas[].background_asset_url,
        areas[].order, area_files) va doi GIAI DOAN 7c PHAI bao loi.
    (B2) [XOA KHOA] Cung nhung ban sao ay, nhung XOA HAN khoa - bao gom ca khoa guong
        grants_flag trong chapter_01.json. Bo qua area_files (muc o do la chuoi tran,
        khong co khoa de xoa).
  Diem nao bi dot bien ma van bao sach la bang chung trinh kiem khong thuc su doc truong
  do. Thoat 0 chi khi CA HAI toan tu deu dat 100%.

  VI SAO PHAI CO TOAN TU THU HAI: ban truoc chi co DOI GIA TRI, va mot toan tu chi biet
  doi gia tri thi chi tham do duoc nhung khoa DANG CO MAT. No mu hoan toan truoc lop lo
  hong "khoa vang mat khong ai gac" - va vi mu nen no van in "DAT (100%)" trong khi 68
  trong 82 khoa guong cua puzzle_index + jumpscare_index bi xoa han van thoat 0. Chinh
  ban tu kiem da tu bao cao rong hon pham vi no tham do, dung kieu loi no sinh ra de bat.

THU MUC DATA MAC DINH:
  Suy ra TUONG DOI tu vi tri file script (<tools>/../data), khong go cung duong dan tuyet
  doi nao. Nho vay mot ban sao du an chay trinh kiem cua chinh no thi kiem du lieu cua
  chinh no, thay vi im lang kiem cay thu muc goc.

Ma thoat: 0 = sach (co the con [CANH BAO]), 1 = co it nhat mot [LOI].
Voi --strict thi MOI [CANH BAO] duoc nang thanh [LOI] (dung cho cong CI).

Vi du:
    python3 tools/validate_level.py
    python3 tools/validate_level.py /duong/dan/khac/data
    python3 tools/validate_level.py --liveops data/liveops_chapter_01.json
    python3 tools/validate_level.py --strict --trace
    python3 tools/validate_level.py --self-test
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

# THU MUC DATA MAC DINH - SUY RA TUONG DOI TU VI TRI CUA CHINH FILE SCRIPT.
#
# Ban truoc go cung "/home/user/HackTheBox/LinhAnThon/data" vao day. Do la mot KET LUAN
# NGUY dung kieu ba vong truoc da phai sua: chay trinh kiem tu MOT BAN SAO khac (ban sao da
# dot bien de thu nghiem, hoac mot checkout khac tren may khac) thi no van IM LANG kiem thu
# muc goc va bao "sach", trong khi nguoi chay dang doc ket luan ay nhu ket luan ve ban sao
# truoc mat ho. Trinh kiem tra loi cho MOT cay thu muc ma nguoi dung tuong la cay khac.
#
# Tu ban nay: <thu muc chua script>/.. /data. Mot ban sao toan bo du an chay trinh kiem cua
# chinh no thi kiem du lieu cua chinh no. Van giu tham so vi tri tren dong lenh de tro toi
# thu muc data khac khi that su can.
#
# Dung abspath chu KHONG dung realpath: neu ai do symlink tools/validate_level.py tu mot noi
# khac vao mot checkout, cai can kiem la checkout dang chua symlink ay, khong phai noi file
# goc nam.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_DATA_DIR = os.path.join(PROJECT_ROOT, "data")

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
# NGUONG CHINH THUC LA 120. 88 KHONG con la mot nguong thay the - no chi la muc do NANG
# HON cua cung mot vi pham:
#
#   canh < MIN_TOUCH_SIZE     (120)  -> [CANH BAO]  chua dat nguong chinh thuc
#   canh < HARD_MIN_TOUCH_SIZE (88)  -> [LOI]       vi pham nang, khong ngoai le
#
# visual_bounds KHONG con mien tru cho canh bao 120. Ly do: visual_bounds co nghia la vung
# cham LON HON hinh ve - no la bien phap BU cho phan con thieu o lop may 640 dp, chu khong
# phai giay phep thu nho vung cham. Dung no de mien tru la dung ca hai dau cua mot lap luan
# cung mot luc.
MIN_TOUCH_SIZE = 120
HARD_MIN_TOUCH_SIZE = 88

# So bat bien LiveOps ma check_liveops() THAT SU hien thuc. Doi chieu voi so dong trong
# data/liveops_chapter_01.json -> validation.invariants. Hai con so lech nhau la [LOI]:
# mot bat bien duoc khai ma khong ai kiem thi no khong ton tai, du no nam trong file.
# Bat bien 17 la cai vua them: iap.products[*].requires.flag phai co nguon cap that.
#
# Danh sach nay duoc DUY TRI BANG TAY (khong co registry tu dang ky), nhung viec ghi ten
# tung bat bien thay vi go mot con so tran co hai cai loi: (1) con so duoi day duoc SINH RA
# bang len(), khong the lech khoi danh sach; (2) them mot phep kiem ma quen them ten vao day
# se lo ra ngay khi doi chieu, thay vi tang thang mot con so khong ai doc duoc.
LIVEOPS_INVARIANTS_IMPLEMENTED = (
    "hint_tier_gem_cost_tang_dan",
    "hint_tier_unlock_free_tang_dan",
    "hint_tier3_trong_max_wait",
    "hint_free_path_guaranteed",
    "iap_product_id_duy_nhat",
    "iap_regional_pricing_du_vung",
    "event_start_truoc_event_end",
    "event_khong_chong_cua_so",
    "event_override_bg_trong_bundles",
    "event_theme_khong_doi_gameplay",
    "ads_chan_trong_va_sau_jumpscare",
    "no_loot_box",
    "telemetry_event_name_hop_le",
    "ab_test_allocation_cong_100",
    "remote_config_key_duy_nhat",
    "gem_economy_earn_du_bu_spend",
    "iap_requires_flag_co_nguon_cap",
)
N_LIVEOPS_INVARIANTS_IMPLEMENTED = len(LIVEOPS_INVARIANTS_IMPLEMENTED)

# KHOA MASTER FORM CUA HOTSPOT - phai CO MAT tren moi hotspot, ke ca khi khong ap dung
# (luc do ghi null). Ba khoa dau (id / bounds / action_type) duoc kiem rieng vi thieu chung
# thi khong con gi de kiem tiep; bon khoa duoi day duoc kiem thanh mot cum.
#
# Vong truoc noi long dung luat nay - "USE_ITEM khong trao gi thi bo item_id di cho gon" -
# va vi schema cung noi long cung luc nen khong lop nao bat duoc. Tu ban nay: thieu khoa
# la [LOI], o ca hai lop.
MASTER_FORM_HOTSPOT_KEYS = ("item_id", "required_item", "target_puzzle_id", "target_area_id")

# Khoa Master Form cua puzzle va jumpscare (ngoai 'id').
MASTER_FORM_PUZZLE_KEYS = ("type", "solution", "required_items", "reward_item_id",
                           "grants_flag", "wrong_action_jumpscare")
MASTER_FORM_SCARE_KEYS = ("trigger_type", "max_fails", "audio_asset", "sprite_animation",
                          "screen_flash")

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
        self._section_title()
        self._current[1].append(line)

    def _section_title(self) -> str:
        """Ten giai doan dang mo. --self-test can biet LOP NAO bat duoc mot dot bien."""
        if self._current is None:
            self.section("KHAC")
        return self._current[0]

    # -- ba muc do -----------------------------------------------------------
    def error(self, where: str, message: str, fix: str = "") -> None:
        self.errors.append((where, message, self._section_title()))
        line = "  %s %s\n      %s" % (self.p.red("[LOI]"), self.p.bold(where), message)
        if fix:
            line += "\n      %s %s" % (self.p.dim("Cach sua:"), self.p.dim(fix))
        self._push(line)

    def warn(self, where: str, message: str, fix: str = "") -> None:
        if self.strict:
            # --strict: canh bao KHONG con la canh bao.
            self.errors.append((where, message, self._section_title()))
            line = "  %s %s\n      %s" % (
                self.p.red("[LOI]"), self.p.bold(where),
                message + self.p.dim("  (nang tu [CANH BAO] vi dang chay --strict)"))
            if fix:
                line += "\n      %s %s" % (self.p.dim("Cach sua:"), self.p.dim(fix))
            self._push(line)
            return
        self.warnings.append((where, message, self._section_title()))
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
            # "du lieu sach hoan toan" la mot cau RONG HON pham vi cua trinh kiem: no
            # noi ve DU LIEU, trong khi cai dem duoc chi la so [LOI] cua nhung phep kiem
            # ma file nay hien thuc. Chinh cau chu nay tung duoc in ra trong khi mo phong
            # con canh ao va manifest con ban sao khong ai gac (xem docstring dau file).
            verdict = self.p.green("DAT - khong [LOI] nao trong pham vi cac giai doan da "
                                   "chay.")
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

def check_bounds(bounds, rep: Report, where: str,
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
            check_touch_size(w, h, rep, where)
    return True


def check_touch_size(w: int, h: int, rep: Report, where: str) -> None:
    """
    GIAI DOAN 4 - nguong vung cham hai muc.

      canh < 120 px @1920 -> [CANH BAO]  : chua dat nguong CHINH THUC
      canh < 88  px @1920 -> [LOI]       : vi pham nang, khong ngoai le

    Khai bao visual_bounds KHONG mien tru gi ca (xem ghi chu o hang so MIN_TOUCH_SIZE).
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
        rep.warn(
            where,
            "Vung cham %dx%d co canh %d px @1920, chua dat NGUONG CHINH THUC %d px "
            "(khoang %d-%d pt tren may that, duoi nguong 44 pt cua Apple HIG)."
            % (w, h, small_edge, MIN_TOUCH_SIZE,
               int(small_edge * 0.33), int(small_edge * 0.49)),
            "No 'bounds' len >= %d px moi canh - vung cham KHONG bat buoc trung voi hinh ve: "
            "giu nguyen sprite va khai bao 'visual_bounds' bang dung vung ve. Luu y "
            "visual_bounds khong mien tru nguong nay, no chi noi ro sprite nho hon vung cham."
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


# Gioi han do dai van xuoi, CHEP DUNG tu maxLength trong schema/level.schema.json
# ($defs.ghi_chu_vi va thuoc tinh 'ten_vi' cua hotspot / puzzle / jumpscare).
#
# Vi sao can: schema dat gioi han nhung KHONG AI THI HANH no - du an khong cai jsonschema,
# nen schema chi la van ban cho toi khi trinh kiem nay kiem ho. Mot ghi chu dai gap doi gioi
# han van di duoc qua toan bo 11 giai doan. Vong nay phat hien dung luc dang sua ghi_chu_vi
# cua hs_hinh_nhan: ban nhap dai 872 ky tu, gap 1.7 lan gioi han 500, va khong lop nao keu.
SCHEMA_TEXT_MAXLEN = {
    "ghi_chu_vi": 500,
    "ten_vi": 120,
}


def check_text_limits(obj, rep: Report, where: str) -> None:
    """GIAI DOAN 2 - do dai van xuoi phai nam trong gioi han schema da dat."""
    if not is_dict(obj):
        return
    for key, limit in sorted(SCHEMA_TEXT_MAXLEN.items()):
        val = obj.get(key)
        if is_str(val) and len(val) > limit:
            rep.error(where,
                      "'%s' dai %d ky tu, vuot gioi han maxLength = %d cua "
                      "schema/level.schema.json." % (key, len(val), limit),
                      "Rut gon con <= %d ky tu, hoac chuyen phan dai sang docs/ va de lai mot "
                      "cau tro toi muc tai lieu do." % limit)


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
    check_text_limits(hs, rep, where)

    if not hs_id.startswith(PREFIX["hotspot"]):
        rep.error(where, "Id hotspot phai bat dau bang tien to '%s'." % PREFIX["hotspot"])
    if not RE_SNAKE.match(hs_id):
        rep.error(where, "Id '%s' khong dung snake_case khong dau." % hs_id)

    if "bounds" not in hs:
        rep.error(where, "Thieu truong bat buoc 'bounds'.")
    else:
        check_bounds(hs["bounds"], rep, where)
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

    # ---- KHOA MASTER FORM: bon khoa nay CO MAT tren MOI hotspot ------------
    #
    # Khong ngoai le, khong "cho nay khong dung thi bo di cho gon". Cho nao khong ap dung
    # thi gia tri la null. Day chinh la cho vong truoc bi thung: item_id bi go khoi bon
    # hotspot USE_ITEM, va vi ca schema lan trinh kiem cung noi long mot luc nen khong ai
    # bat duoc. Kiem SU CO MAT cua khoa, khong chi kiem gia tri.
    for key in MASTER_FORM_HOTSPOT_KEYS:
        if key not in hs:
            rep.error(
                where,
                "Thieu khoa Master Form '%s'. Moi hotspot phai mang DU bon khoa %s - cho nao "
                "khong ap dung thi ghi null, khong duoc xoa khoa. Khoa vang mat va khoa mang "
                "gia tri null la hai trang thai khac nhau: cai dau la du lieu khong day du "
                "(khong ai biet designer da can nhac chua), cai sau la mot quyet dinh duoc "
                "ghi lai." % (key, fmt_list(MASTER_FORM_HOTSPOT_KEYS)),
                "Them \"%s\": null vao hotspot nay." % key,
            )

    # ---- rang buoc co dieu kien theo action_type ---------------------------
    if action == "ZOOM_PUZZLE":
        if not is_str(hs.get("target_puzzle_id")):
            rep.error(where, "ZOOM_PUZZLE bat buoc co 'target_puzzle_id' KHAC null, tro toi "
                             "mot puzzle trong CUNG file area.")

    elif action == "COLLECT_ITEM":
        if not is_str(hs.get("item_id")):
            rep.error(where, "COLLECT_ITEM bat buoc co 'item_id' KHAC null (chuoi).")
        if hs.get("required_item") is not None and not is_str(hs.get("required_item")):
            rep.error(where, "'required_item' phai la item_id hoac null.")

    elif action == "USE_ITEM":
        req = hs.get("required_item")
        if not is_str(req):
            rep.error(where, "USE_ITEM bat buoc co 'required_item' KHAC null - "
                             "phai noi ro dung vat pham nao.")
        # Hieu ung hop le cua USE_ITEM: trao vat pham MOI, mo cau do, mo duong sang khu vuc,
        # hoac - dang hay gap nhat o Chuong 1 - chi de lai mot co tien trinh ("dat vat pham
        # vao cho" ma khong tieu huy, khong trao gi moi). check_use_item_noop() bao gom ca bon.
        check_use_item_noop(hs, rep, where)
        check_consume_semantics(hs, rep, where)

    elif action == "CHANGE_AREA":
        if not is_str(hs.get("target_area_id")):
            rep.error(where, "CHANGE_AREA bat buoc co 'target_area_id' KHAC null, tro toi mot "
                             "area co trong chapter manifest.")

    elif action in ("EXAMINE", "DIALOGUE"):
        tk = hs.get("text_key")
        if not is_str(tk):
            rep.error(where, "%s bat buoc co 'text_key' (khoa localization, vd "
                             "'txt_examine_ban_tho')." % action)
        elif not RE_TEXT_KEY.match(tk):
            rep.error(where, "text_key '%s' sai quy uoc - phai khop ^txt_[a-z0-9_]+$." % tk)
        for forbidden in MASTER_FORM_HOTSPOT_KEYS:
            if hs.get(forbidden) is not None:
                rep.error(where, "%s co '%s' = %r. Bon khoa hanh dong van PHAI CO MAT tren "
                                 "hotspot nay, nhung gia tri phai la null: mot hotspot chi de "
                                 "doc chu khong trao vat pham, khong mo cau do, khong doi khu "
                                 "vuc." % (action, forbidden, hs.get(forbidden)),
                          "Dat \"%s\": null." % forbidden)

    if action != "USE_ITEM":
        for forbidden in ("consumes_item", "locks_item"):
            if forbidden in hs:
                rep.error(where, "'%s' chi thuoc ve hotspot USE_ITEM, nhung hotspot nay la "
                                 "%s. O day no khong co nghia gi va se bi engine lo di."
                          % (forbidden, action),
                          "Bo truong '%s' khoi hotspot nay." % forbidden)

    if action != "CHANGE_AREA" and hs.get("target_area_id") is not None:
        rep.error(where, "Chi CHANGE_AREA moi duoc mang 'target_area_id' khac null, hotspot "
                         "nay la %s." % action)

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


def check_consume_semantics(hs, rep: Report, where: str) -> None:
    """
    GIAI DOAN 3 - NGU NGHIA TIEU HAO VAT PHAM PHAI DOC DUOC BANG MAY.

    Truoc ban nay, khong mot truong nao noi len viec dung vat pham co tieu huy no hay khong -
    chi co van xuoi tieng Viet trong 'ghi_chu_vi', va hai hotspot con mo ta hanh vi NGUOC
    NHAU. Hau qua: ca mo phong cua du an lan mo phong doc lap cua auditor deu phai TU CHON
    gia dinh "khong tieu hao" thi moi ket luan duoc kha giai. Neu engine tieu huy dong nhat
    thi chuong tut xuong 4/5 khu vuc va co ket chuong khong bao gio bat len.

    Nay moi hotspot USE_ITEM phai khai bao:
      consumes_item  BAT BUOC tren moi hotspot USE_ITEM.
                     true  = vat pham bi XOA HAN khoi tui do sau khi dung
                     false = vat pham o lai
      locks_item     BAT BUOC khi consumes_item = false, BI CAM khi consumes_item = true.
                     true  = o lai nhung bi KHOA: khong keo-tha len hotspot khac duoc nua
                     false = o lai va dung tiep tu do
    """
    if "consumes_item" not in hs:
        rep.error(
            where,
            "Hotspot USE_ITEM khong khai bao 'consumes_item'. Khong co truong nay thi ngu "
            "nghia tieu hao chi ton tai trong van xuoi: engine phai doan, mo phong kha giai "
            "phai doan, va hai ben doan khac nhau la chuong hoac soft-lock hoac di duoc bang "
            "mot duong khong co that.",
            "Them \"consumes_item\": true neu dung xong vat pham bien mat khoi tui do, hoac "
            "false neu no o lai. Can cu y do thiet ke: docs/01_KICH_BAN_CHAPTER_01.md muc 4.3.",
        )
    elif not is_bool(hs["consumes_item"]):
        rep.error(where, "'consumes_item' phai la true hoac false, dang nhan %r."
                  % (hs["consumes_item"],))

    # 'locks_item' LA MOT TRUONG CHINH THUC, va su co mat cua no duoc quyet dinh HOAN TOAN
    # boi 'consumes_item' - khong con vung xam "co cung duoc, khong cung duoc":
    #
    #   consumes_item = false  ->  locks_item BAT BUOC co mat (true hoac false).
    #   consumes_item = true   ->  locks_item BI CAM (vat pham da mat han thi khong the
    #                              dong thoi "o lai trong tui nhung bi khoa").
    #
    # Ly do siet chieu thu nhat: truoc ban nay, ba trong bon hotspot USE_ITEM khai locks_item
    # con mot cai thi khong, va khong lop nao noi duoc do la co y hay bo sot. Vang mat mot
    # truong boolean thi nguoi doc phai TU CHON mot gia dinh ve gia tri mac dinh - dung kieu
    # mo ho ma vong nay di don. Chieu thu hai giu nguyen luat cu (mau thuan im lang).
    if "locks_item" in hs:
        if not is_bool(hs["locks_item"]):
            rep.error(where, "'locks_item' phai la true hoac false, dang nhan %r."
                      % (hs["locks_item"],))
        elif hs.get("consumes_item") is True:
            rep.error(
                where,
                "Khai bao dong thoi \"consumes_item\": true va 'locks_item' - mau thuan. Vat "
                "pham da bi xoa han khoi tui do thi khong the dong thoi \"o lai trong tui "
                "nhung bi khoa\".",
                "Giu mot trong hai: consumes_item true (mat han, va KHONG khai locks_item), "
                "hoac consumes_item false kem locks_item true (o lai, xam di, khong dung lai "
                "duoc).",
            )
    elif hs.get("consumes_item") is False:
        rep.error(
            where,
            "Hotspot USE_ITEM co \"consumes_item\": false nhung khong khai bao 'locks_item'. "
            "Vat pham o lai trong tui do - con dung lai duoc hay bi khoa lai la hai hanh vi "
            "khac han nhau, va o day khong truong nao noi len dieu do.",
            "Them \"locks_item\": false neu vat pham van keo-tha tu do duoc, hoac true neu no "
            "o lai nhung bi khoa (xam di, chi con EXAMINE duoc).",
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
    check_text_limits(pz, rep, where)

    if not pz_id.startswith(PREFIX["puzzle"]):
        rep.error(where, "Id puzzle phai bat dau bang tien to '%s'." % PREFIX["puzzle"])
    if not RE_SNAKE.match(pz_id):
        rep.error(where, "Id '%s' khong dung snake_case khong dau." % pz_id)

    # ---- KHOA MASTER FORM ---------------------------------------------------
    for key in MASTER_FORM_PUZZLE_KEYS:
        if key not in pz:
            rep.error(where, "Thieu khoa Master Form '%s' cua puzzle." % key,
                      "Moi puzzle phai mang du %s." % fmt_list(MASTER_FORM_PUZZLE_KEYS))

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

    # ---- grants_flag: BAT BUOC, TUONG MINH, KHONG duoc null ----------------
    #
    # Khong con luat suy dien nao sinh co tu puzzle_id nua (xem build_flag_producers).
    # Cau do khong ghi grants_flag la cau do khong bat co gi ca - va moi cho dang cho
    # "flag_<cau do nay>_solved" se ket cung vinh vien.
    gf = pz.get("grants_flag")
    if gf is None:
        rep.error(
            where,
            "'grants_flag' bi bo trong. Truoc day trinh kiem tu bu vao bang cong thuc "
            "'flag_%s_solved' - mot canh AO dung TEN DINH DANH chu khong dung du lieu, va "
            "chinh no da tung lam trinh kiem bao \"du lieu sach hoan toan\" cho mot ban du "
            "lieu bi xoa mat nguon cap co. Canh do da bi go bo, nen gio truong nay bat buoc."
            % pz_id,
            "Them \"grants_flag\": \"flag_%s_solved\" vao cau do nay (quy uoc DAT TEN van "
            "the, nhung gia tri phai duoc ghi thang ra trong JSON)." % pz_id,
        )
    elif not is_str(gf):
        rep.error(where, "'grants_flag' phai la flag_id (chuoi), dang nhan %r." % (gf,))
    elif not gf.startswith(PREFIX["flag"]):
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
    check_text_limits(js, rep, where)

    if not js_id.startswith(PREFIX["jumpscare"]):
        rep.error(where, "Id jumpscare phai bat dau bang tien to '%s'." % PREFIX["jumpscare"])
    if not RE_SNAKE.match(js_id):
        rep.error(where, "Id '%s' khong dung snake_case khong dau." % js_id)

    # ---- KHOA MASTER FORM ---------------------------------------------------
    for key in MASTER_FORM_SCARE_KEYS:
        if key not in js:
            rep.error(where, "Thieu khoa Master Form '%s' cua jumpscare." % key,
                      "Moi jumpscare phai mang du %s - 'max_fails' ghi null khi "
                      "trigger_type khong phai ON_PUZZLE_FAIL_COUNT."
                      % fmt_list(MASTER_FORM_SCARE_KEYS))

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
        if "max_fails" in js and js["max_fails"] is not None:
            rep.error(where, "trigger_type '%s' co 'max_fails' = %r. Khoa nay VAN PHAI CO MAT "
                             "(no thuoc Master Form) nhung gia tri phai la null - khong co bo "
                             "dem giai sai nao chay cho loai trigger nay."
                      % (trig, js["max_fails"]),
                      "Dat \"max_fails\": null.")

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
    # doa xung. docs/01_KICH_BAN_CHAPTER_01.md muc 6.6 dinh nghia luat mien tru la:
    # impulse == false VA
    # screen_flash == false VA camera_punch_pct == 0 VA haptic_pattern_at_0ms == null.
    # Trong hop dong du lieu hien tai, chi 'screen_flash' la doc duoc bang may - nen day la
    # dieu kien CAN duy nhat may kiem duoc, va no phai duoc kiem. Mot cu doa vua chop man
    # vua tu nhan mien tru cooldown la mot impulse scare ban lai khong gioi han: dung cai
    # ma luat cooldown sinh ra de chan.
    if js.get("cooldown_exempt") is True and js.get("screen_flash") is True:
        rep.error(where, "Khai bao \"cooldown_exempt\": true nhung 'screen_flash' = true - "
                         "mien tru cooldown chi danh cho dread scare (khong transient, khong "
                         "flash, khong punch, khong haptic o moc 0 ms) theo "
                         "docs/01_KICH_BAN_CHAPTER_01.md muc 6.6, va chinh sach nhap nhay o "
                         "docs/06_AN_TOAN_NGUOI_CHOI.md muc 2.3. Mot cu doa co chop man la "
                         "impulse scare, va impulse scare "
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
        # Doi tuong manifest THO, giu nguyen. GIAI DOAN 7c can doc nhung khoi ma manifest
        # LAP LAI tu file khu vuc (puzzle_index, jumpscare_index, flag_registry, ...) de doi
        # chieu guong voi gia tri that. Truoc ban nay khong ham nao trong trinh kiem doc toi
        # chung, nen mot ban sao lech trong manifest khong lop nao bat duoc.
        self.manifest = {}
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
        self.complete_flag = None  # co KET CHUONG, khai bao tuong minh o manifest

    def area_hotspots(self, area_id):
        area = self.areas.get(area_id) or {}
        return [hs for hs in area.get("hotspots", []) if is_dict(hs) and is_str(hs.get("id"))]

    def item_delivery_hotspots(self):
        """
        item_id -> danh sach hotspot COLLECT_ITEM THUC SU dat vat pham vao tui do.

        Doc thang tu cau truc du lieu (action_type + item_id), khong doc tu ten, khong doc
        tu van xuoi ghi_chu_vi. Dung cho luat giao phan thuong o GIAI DOAN 10.
        """
        out = defaultdict(list)
        for hs_id, (area_id, hs) in self.hotspots.items():
            if hs.get("action_type") == "COLLECT_ITEM" and is_str(hs.get("item_id")):
                out[hs["item_id"]].append(hs_id)
        return dict(out)

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
        # Liet ke DU nhung truong vong tren that su duyet. Mot danh sach cat ngan khien
        # nguoi doc tuong pham vi hep hon thuc te; mot danh sach phong len thi nguoc lai.
        rep.ok("Toan bo tham chieu cheo deu tro toi doi tuong co that: target_puzzle_id, "
               "target_area_id, hotspot.item_id, hotspot.required_item, "
               "wrong_action_jumpscare, puzzle.reward_item_id, puzzle.required_items, "
               "jumpscare.trigger_item_id, unlock_condition.{required_items, from_area_id, "
               "entry_hotspot_id}, item_catalog.{nguon, nhat_o_area}.")


# --------------------------------------------------------------------------
# GIAI DOAN 7c: DOI CHIEU GUONG - MANIFEST CHEP LAI GIA TRI CUA FILE KHU VUC
# --------------------------------------------------------------------------
#
# data/chapter_01.json khong chi khai bao thu tu khu vuc. No con CHEP LAI hang loat gia tri
# von thuoc ve data/areas/*.json: puzzle_index lap lai type / reward_item_id / required_items
# / grants_flag cua ca 6 cau do, jumpscare_index lap lai trigger_type / max_fails / delay_sec
# / cooldown_sec cua 8 cu doa, flag_registry lap lai nguon cap cua tung co, moi muc trong
# 'areas' lap lai background_asset_url cua file khu vuc, va 'area_files' lap lai 'file'.
#
# Truoc ban nay, KHONG mot ham nao trong trinh kiem doc toi nhung khoi ay. Chung la ban sao
# khong ai doi chieu: sua puzzle_index[2].grants_flag thanh mot ten co khac thi ca 11 giai
# doan deu im lang va trinh kiem van in "DAT - du lieu sach hoan toan". Do dung la kieu loi
# ma ba vong truoc mac phai o phia tai lieu - con so duoc chep qua lai giua cac file ma
# khong ai dem lai tu nguon - nhung lan nay no nam ngay trong du lieu.
#
# Luat cua giai doan nay: cai gi duoc LAP LAI thi phai TRUNG KHOP gia tri THAT, va cai gi
# co that thi phai co mat trong ban sao. Mot khoa duoc lap lai ma trinh kiem khong biet
# cach doi chieu -> [CANH BAO], vi do lai la mot ban sao khong ai gac.
#
# BAN TRUOC TUYEN BO CAU TREN NHUNG CHI LAM DUOC MOT NUA, va do chinh la kieu loi ma du an
# nay da vap bon lan: mot phep kiem tu bao cao rong hon nhung gi no thuc su kiem. Ve chieu
# "co that thi phai co mat trong ban sao", no chi gac o MUC BAN GHI (thieu han mot muc
# puzzle_index -> bao loi). O MUC TUNG TRUONG no chi duyet nhung khoa CON NAM trong
# manifest ("for key in sorted(entry)"), nen XOA HAN mot khoa guong la lot sach: quet rong
# cho thay 68 trong 82 khoa guong cua puzzle_index + jumpscare_index bi xoa deu khong bi
# bat, trinh kiem van in "DAT - du lieu sach hoan toan" va thoat 0. Chi 14 khoa dinh danh
# (puzzle_id / scare_id) bi bat, va bat vi mot ly do khac: muc index mat dinh danh.
#
# Tu ban nay, ca 7c.1, 7c.2 va 7c.4 duyet HOP (union) cac khoa cua ban guong va ban goc:
#   - khoa co o goc ma thieu o guong   -> [LOI] BAN SAO THIEU KHOA
#   - khoa co o guong ma thieu o goc   -> [LOI]
#   - khoa co o ca hai ma lech gia tri -> [LOI] LECH BAN SAO
# 7c.3 (flag_registry) von da hai chieu san: no so sanh CA BO ba (nguon_kieu, nguon_id,
# area_id) dung .get(), nen xoa mot khoa bien bo ba thanh lech va van bao loi.

_ABSENT = object()

# Khoa trong muc index -> cach lay GIA TRI THAT tu doi tuong trong file khu vuc:
#   "id"    doi chieu voi truong 'id' cua doi tuong that
#   "area"  doi chieu voi khu vuc THUC SU chua doi tuong (doc tu file dang nap no)
#   "field" doi chieu voi truong CUNG TEN tren doi tuong that
PUZZLE_INDEX_MIRROR = {
    "puzzle_id": "id",
    "area_id": "area",
    "type": "field",
    "reward_item_id": "field",
    "required_items": "field",
    "grants_flag": "field",
}

JUMPSCARE_INDEX_MIRROR = {
    "scare_id": "id",
    "area_id": "area",
    "trigger_type": "field",
    "trigger_item_id": "field",
    "max_fails": "field",
    "delay_sec": "field",
    "cooldown_sec": "field",
    "cooldown_exempt": "field",
}

FLAG_REGISTRY_MIRROR = ("flag_id", "nguon_kieu", "nguon_id", "area_id")

# Van xuoi mo ta / chu thich: khong phai ban sao cua truong nao, khong doi chieu.
MIRROR_PROSE_KEYS = ("mo_ta_vi", "ghi_chu_vi", "ten_vi", "duoc_doc_boi", "dung_cho")

# nguon_kieu cua flag_registry <-> loai nguon cap ma build_flag_producers() ghi nhan.
FLAG_SOURCE_KIND = {"PUZZLE": "puzzle", "HOTSPOT": "hotspot"}


def mirror_equal(a, b) -> bool:
    """
    So sanh hai gia tri JSON cho phep doi chieu guong.

    Nghiem ngat o dung mot cho ma dau '==' cua Python de lot: true == 1. Mot manifest chep
    "cooldown_exempt": 1 thay vi true la mot ban sao SAI, khong phai mot ban sao tuong duong.
    """
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    if is_list(a) != is_list(b):
        return False
    if is_list(a):
        return len(a) == len(b) and all(mirror_equal(x, y) for x, y in zip(a, b))
    return a == b


def _mirror_show(v) -> str:
    if v is _ABSENT:
        return "<khong co truong nay>"
    return json.dumps(v, ensure_ascii=False)


def _check_index_block(ch: Chapter, rep: Report, block_key: str, id_key: str,
                       mirror_map: dict, real_table: dict, ten_that: str):
    """
    Doi chieu mot khoi index cua manifest voi bang doi tuong THAT (ch.puzzles / ch.jumpscares).

    Tra ve (so_truong_da_doi_chieu, so_loi).
    """
    raw = (ch.manifest or {}).get(block_key)
    n_checked = 0
    n_bad = 0
    where_block = "chapter_01.json / %s" % block_key

    if raw is None:
        rep.warn(where_block,
                 "Manifest khong co khoi '%s' - khong co ban sao nao de doi chieu voi %d %s "
                 "co that." % (block_key, len(real_table), ten_that),
                 "Them khoi '%s', hoac bo han neu khong muon duy tri ban sao." % block_key)
        return 0, 0
    if not is_list(raw):
        rep.error(where_block, "'%s' phai la mang." % block_key)
        return 0, 1

    seen = set()
    for idx, entry in enumerate(raw):
        where = "chapter_01.json / %s[%d]" % (block_key, idx)
        if not is_dict(entry):
            rep.error(where, "Muc index phai la doi tuong JSON.")
            n_bad += 1
            continue
        oid = entry.get(id_key)
        if not is_str(oid):
            rep.error(where, "Muc index thieu khoa dinh danh '%s'." % id_key)
            n_bad += 1
            continue
        if oid in seen:
            rep.error(where, "'%s' = '%s' xuat hien nhieu lan trong '%s'."
                      % (id_key, oid, block_key))
            n_bad += 1
        seen.add(oid)
        if oid not in real_table:
            rep.error(where,
                      "Ban sao trong manifest tro toi %s '%s' KHONG CO THAT trong "
                      "data/areas/*.json." % (ten_that, oid),
                      "Xoa muc index nay, hoac sua '%s' cho dung dinh danh that." % id_key)
            n_bad += 1
            continue

        area_id, obj = real_table[oid]

        # Khoa manifest lap lai ma KHONG co luat doi chieu -> ban sao khong ai gac.
        for key in sorted(entry):
            if key in mirror_map or key in MIRROR_PROSE_KEYS:
                continue
            rep.warn(where,
                     "Manifest lap lai khoa '%s' nhung trinh kiem khong co luat doi chieu "
                     "cho no - day lai la mot ban sao khong ai gac." % key,
                     "Them '%s' vao bang doi chieu guong trong tools/validate_level.py, "
                     "hoac bo khoa nay khoi manifest." % key)

        # DUYET HOP (union) cac khoa cua BAN GUONG va BAN GOC, khong duyet rieng ban guong.
        #
        # Duyet "for key in sorted(entry)" chi nhin thay nhung khoa CON NAM trong manifest,
        # nen XOA HAN mot khoa guong la cach lam lech ban sao ma no khong the thay: 68/82
        # khoa guong bi xoa deu thoat 0. Mot phep gac chi mot chieu ma nhan la hai chieu
        # chinh la kieu loi ma cac vong truoc mac phai. Tu ban nay: moi khoa trong
        # mirror_map deu duoc xet, du no vang mat o ben nao.
        for key in sorted(mirror_map):
            role = mirror_map[key]
            if role == "id":
                real = obj.get("id", _ABSENT)
            elif role == "area":
                real = area_id
            else:
                real = obj.get(key, _ABSENT)
            copied = entry.get(key, _ABSENT)

            # Ca hai ben deu khong khai bao: khong co ban sao nao ton tai o day.
            if copied is _ABSENT and real is _ABSENT:
                continue

            n_checked += 1
            if real is _ABSENT:
                # Co o guong, thieu o goc.
                rep.error(where,
                          "Manifest chep '%s' = %s, nhung %s '%s' co that KHONG khai bao "
                          "truong '%s'." % (key, _mirror_show(copied), ten_that, oid, key),
                          "Bo khoa '%s' khoi muc index, hoac khai bao no o file khu vuc %s."
                          % (key, area_id))
                n_bad += 1
            elif copied is _ABSENT:
                # Co o goc, thieu o guong.
                rep.error(where,
                          "BAN SAO THIEU KHOA: %s '%s' trong %s khai bao '%s' = %s, nhung "
                          "muc index trong manifest KHONG chep lai khoa '%s' - moi thu doc "
                          "manifest de liet ke se khong thay gia tri nay."
                          % (ten_that, oid, area_id, key, _mirror_show(real), key),
                          "Them \"%s\": %s vao muc index nay."
                          % (key, _mirror_show(real)))
                n_bad += 1
            elif not mirror_equal(copied, real):
                rep.error(where,
                          "LECH BAN SAO: manifest chep '%s' = %s, gia tri THAT cua %s '%s' "
                          "trong %s la %s."
                          % (key, _mirror_show(copied), ten_that, oid, area_id,
                             _mirror_show(real)),
                          "File khu vuc la nguon su that. Sua manifest cho khop, dung sua "
                          "nguoc lai tru khi chinh file khu vuc moi la cai sai.")
                n_bad += 1

    for oid in sorted(real_table):
        if oid not in seen:
            area_id, _obj = real_table[oid]
            rep.error(where_block,
                      "%s '%s' (%s) co that nhung KHONG co trong '%s' - ban sao thieu muc, "
                      "moi thu doc manifest de liet ke se bo sot no."
                      % (ten_that.capitalize(), oid, area_id, block_key),
                      "Them mot muc cho '%s' vao '%s'." % (oid, block_key))
            n_bad += 1

    return n_checked, n_bad


def check_manifest_mirror(ch: Chapter, rep: Report) -> None:
    """GIAI DOAN 7c - moi gia tri manifest chep lai phai trung khop gia tri that."""
    manifest = ch.manifest or {}
    n_checked = 0
    n_bad = 0

    # -- 7c.1 puzzle_index ---------------------------------------------------
    c, b = _check_index_block(ch, rep, "puzzle_index", "puzzle_id",
                              PUZZLE_INDEX_MIRROR, ch.puzzles, "cau do")
    n_checked += c
    n_bad += b

    # -- 7c.2 jumpscare_index ------------------------------------------------
    c, b = _check_index_block(ch, rep, "jumpscare_index", "scare_id",
                              JUMPSCARE_INDEX_MIRROR, ch.jumpscares, "cu doa")
    n_checked += c
    n_bad += b

    # -- 7c.3 flag_registry --------------------------------------------------
    # Ban sao cua NGUON CAP co tien trinh. Gia tri that la ch.flag_producers, va bang do
    # duoc dung o GIAI DOAN 7a CHI tu gia tri cua truong grants_flag doc trong file khu vuc.
    raw = manifest.get("flag_registry")
    where_block = "chapter_01.json / flag_registry"
    if raw is None:
        rep.warn(where_block, "Manifest khong co khoi 'flag_registry' - khong co ban sao nao "
                              "de doi chieu voi %d co tien trinh co nguon cap that."
                 % len(ch.flag_producers))
    elif not is_list(raw):
        rep.error(where_block, "'flag_registry' phai la mang.")
        n_bad += 1
    else:
        seen_flags = set()
        for idx, entry in enumerate(raw):
            where = "chapter_01.json / flag_registry[%d]" % idx
            if not is_dict(entry):
                rep.error(where, "Muc flag_registry phai la doi tuong JSON.")
                n_bad += 1
                continue
            flag = entry.get("flag_id")
            if not is_str(flag):
                rep.error(where, "Muc flag_registry thieu 'flag_id'.")
                n_bad += 1
                continue
            if flag in seen_flags:
                rep.error(where, "'flag_id' = '%s' xuat hien nhieu lan trong flag_registry."
                          % flag)
                n_bad += 1
            seen_flags.add(flag)

            for key in sorted(entry):
                if key not in FLAG_REGISTRY_MIRROR and key not in MIRROR_PROSE_KEYS:
                    rep.warn(where,
                             "Manifest lap lai khoa '%s' nhung trinh kiem khong co luat doi "
                             "chieu cho no." % key)

            producers = ch.flag_producers.get(flag) or []
            n_checked += 1
            if not producers:
                rep.error(where,
                          "flag_registry khai co '%s' nhung KHONG hotspot/puzzle nao trong "
                          "data/areas/*.json khai \"grants_flag\": \"%s\" - ban sao dang mo ta "
                          "mot nguon cap khong ton tai." % (flag, flag),
                          "Xoa muc nay, hoac them grants_flag that o doi tuong cap co.")
                n_bad += 1
                continue

            # (nguon_kieu, nguon_id, area_id) phai khop DUNG MOT nguon cap that.
            real_triples = [(kind, oid, aid) for kind, oid, aid, _how in producers]
            claim = (FLAG_SOURCE_KIND.get(entry.get("nguon_kieu")),
                     entry.get("nguon_id"), entry.get("area_id"))
            n_checked += 3
            if claim not in real_triples:
                rep.error(where,
                          "LECH BAN SAO: flag_registry khai nguon cap cua '%s' la "
                          "%s '%s' o %s; nguon cap THAT (doc tu grants_flag) la %s."
                          % (flag, entry.get("nguon_kieu"), entry.get("nguon_id"),
                             entry.get("area_id"),
                             fmt_list(["%s '%s' o %s" % (k.upper(), i, a)
                                       for k, i, a in real_triples])),
                          "Sua 'nguon_kieu' / 'nguon_id' / 'area_id' cho khop voi doi tuong "
                          "that su khai grants_flag.")
                n_bad += 1

        for flag in sorted(ch.flag_producers):
            if flag not in seen_flags:
                rep.error(where_block,
                          "Co '%s' co nguon cap that nhung KHONG co trong flag_registry - "
                          "ban sao thieu muc." % flag,
                          "Them mot muc cho '%s' vao flag_registry." % flag)
                n_bad += 1

    # -- 7c.4 areas[]: background_asset_url va order -------------------------
    manifest_areas = [e for e in (manifest.get("areas") or []) if is_dict(e)]
    for idx, entry in enumerate(manifest_areas):
        area_id = entry.get("area_id")
        where = "chapter_01.json / areas[%d]" % idx
        if not is_str(area_id) or area_id not in ch.areas:
            continue        # da bao o cho khac
        area = ch.areas[area_id]

        # Cung luat HAI CHIEU nhu 7c.1/7c.2: khoa vang mat o BEN NAO cung la lech ban sao.
        copied_bg = entry.get("background_asset_url", _ABSENT)
        real_bg = area.get("background_asset_url", _ABSENT)
        if not (copied_bg is _ABSENT and real_bg is _ABSENT):
            n_checked += 1
            if copied_bg is _ABSENT:
                rep.error(where,
                          "BAN SAO THIEU KHOA: file khu vuc '%s' khai bao background_asset_url "
                          "= %s, nhung muc areas[%d] trong manifest KHONG chep lai khoa nay."
                          % (area_id, _mirror_show(real_bg), idx),
                          "Them \"background_asset_url\": %s vao muc areas[%d]."
                          % (_mirror_show(real_bg), idx))
                n_bad += 1
            elif not mirror_equal(copied_bg, real_bg):
                rep.error(where,
                          "LECH BAN SAO: manifest chep background_asset_url = %s cho '%s', "
                          "gia tri THAT trong file khu vuc la %s."
                          % (_mirror_show(copied_bg), area_id, _mirror_show(real_bg)),
                          "Engine nap anh nen tu file khu vuc; ban sao trong manifest lech di "
                          "la mot lo trinh bay sai cho moi cong cu doc manifest.")
                n_bad += 1

        copied_order = entry.get("order", _ABSENT)
        real_order = ch.area_order.index(area_id) + 1 if area_id in ch.area_order else _ABSENT
        if not (copied_order is _ABSENT and real_order is _ABSENT):
            n_checked += 1
            if copied_order is _ABSENT:
                rep.error(where,
                          "BAN SAO THIEU KHOA: '%s' dung thu %s trong 'area_order', nhung muc "
                          "areas[%d] trong manifest KHONG chep lai khoa 'order'."
                          % (area_id, _mirror_show(real_order), idx),
                          "Them \"order\": %s vao muc areas[%d]."
                          % (_mirror_show(real_order), idx))
                n_bad += 1
            elif not mirror_equal(copied_order, real_order):
                rep.error(where,
                          "LECH BAN SAO: areas[%d].order = %s cho '%s', nhung vi tri THAT cua "
                          "khu vuc nay trong 'area_order' la %s."
                          % (idx, _mirror_show(copied_order), area_id,
                             _mirror_show(real_order)),
                          "'area_order' la thu tu that; 'order' chi la ban sao de doc cho de.")
                n_bad += 1

    # -- 7c.5 area_files <-> areas[].file ------------------------------------
    area_files = manifest.get("area_files")
    if area_files is not None:
        if not is_list(area_files):
            rep.error("chapter_01.json / area_files", "'area_files' phai la mang duong dan.")
            n_bad += 1
        else:
            real_files = [e.get("file") for e in manifest_areas]
            if len(area_files) != len(real_files):
                rep.error("chapter_01.json / area_files",
                          "'area_files' co %d muc nhung 'areas' co %d muc - hai danh sach la "
                          "ban sao cua nhau." % (len(area_files), len(real_files)),
                          "Giu dung mot muc trong 'area_files' cho moi muc trong 'areas'.")
                n_bad += 1
            else:
                for i, (copied, real) in enumerate(zip(area_files, real_files)):
                    n_checked += 1
                    if not mirror_equal(copied, real):
                        rep.error("chapter_01.json / area_files[%d]" % i,
                                  "LECH BAN SAO: area_files[%d] = %s nhung areas[%d].file = %s."
                                  % (i, _mirror_show(copied), i, _mirror_show(real)),
                                  "'areas[].file' la duong dan THAT su duoc nap; sua "
                                  "'area_files' cho khop.")
                        n_bad += 1

    if not n_bad:
        rep.ok("Doi chieu guong HAI CHIEU tren %d cap khoa (%d cau do, %d cu doa, %d co "
               "tien trinh, %d khu vuc): khong khoa nao thieu o ban guong, khong khoa nao "
               "thieu o ban goc, khong gia tri nao lech."
               % (n_checked, len(ch.puzzles), len(ch.jumpscares), len(ch.flag_producers),
                  len(ch.areas)))


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
    Xac dinh nguon cap cho moi co tien trinh. DUNG MOT NGUON DUY NHAT:

        gia tri cua truong "grants_flag" doc thang tu JSON (tren mot hotspot hoac mot puzzle).

    Khong con nguon thu hai. Cai tung duoc goi la "QUY UOC CHINH TAC" - giai cau do X thi
    bat co "flag_<X>_solved" - da bi GO BO HOAN TOAN. No nghe nhu mot hop dong, nhung cai
    chuoi ay duoc trinh kiem tu tay cap bang cong thuc 'flag_%s_solved' % pz_id, tuc dung
    TEN DINH DANH cua cau do chu khong dung mot truong nao trong du lieu. Bang chung dot
    bien: xoa grants_flag cua puz_tuan_tu_le_cung - nguon cap tuong minh DUY NHAT cua
    flag_puz_tuan_tu_le_cung_solved - thi trinh kiem van in "[OK] KHA GIAI ... 5/5 khu vuc"
    va thoat 0, trong khi mot mo phong doc lap chi di duoc 3/5 khu vuc va 4/6 cau do.
    Mot canh chi ton tai trong trinh kiem, khong ton tai trong du lieu, la mot canh AO.

    Bu lai o phia du lieu: puzzles[].grants_flag la truong BAT BUOC (xem check_puzzle), va
    che do --self-test dot bien tung truong mot de chung to trinh kiem THAT SU doc chung.

    Phan doan ten van con, nhung chi duoi dang [i] GOI Y cho nguoi thiet ke, in o cuoi giai
    doan, va khong ham nao doc lai no.

    Co duoc tham chieu (unlock_condition.required_flags / hotspot.required_flags) ma khong
    co nguon cap nao -> [LOI]. Khong phai [CANH BAO]: khu vuc doi co do khong bao gio mo.
    """
    producers = defaultdict(list)

    for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
        gf = hs.get("grants_flag")
        if is_str(gf):
            producers[gf].append(("hotspot", hs_id, area_id, "tuong minh"))
    for pz_id, (area_id, pz) in sorted(ch.puzzles.items()):
        gf = pz.get("grants_flag")
        if is_str(gf):
            producers[gf].append(("puzzle", pz_id, area_id, "tuong minh"))

    ch.flag_producers = dict(producers)

    # -- doi chieu voi cac co THUC SU duoc tham chieu ------------------------
    refs = collect_flag_references(ch)
    dangling = [flag for flag in sorted(refs) if not producers.get(flag)]

    for flag in dangling:
        rep.error(
            "co tien trinh '%s'" % flag,
            "KHONG co nguon cap: khong mot hotspot hay puzzle nao khai bao \"grants_flag\": "
            "\"%s\". Co nay khong bao gio bat len duoc, nen %d cho dang doi no se ket cung "
            "vinh vien: %s"
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
    # -- co KET CHUONG phai co nguon cap ------------------------------------
    if is_str(ch.complete_flag) and not producers.get(ch.complete_flag):
        rep.error(
            "chapter_01.json / chapter_complete_flag",
            "Co ket chuong '%s' KHONG co nguon cap: khong mot hotspot hay puzzle nao khai "
            "\"grants_flag\": \"%s\". Chuong khong the ket thuc."
            % (ch.complete_flag, ch.complete_flag),
            "Them \"grants_flag\": \"%s\" vao dung hotspot thuc hien hanh dong ket chuong."
            % ch.complete_flag,
        )

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
        if flag in refs or flag in exported or flag == ch.complete_flag:
            continue
        explicit = list(prods)
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

    # Bo dem phai KHOP voi cai duoc in. Ban truoc in cau "Khong co nguon nao duoc suy luan"
    # ngay canh chinh bo dem "+6 theo QUY UOC CHINH TAC" cua no - hai ve cua cung mot dong
    # phu dinh nhau. Gio chi con mot loai nguon, nen chi con mot con so.
    n_hs = sum(1 for prods in producers.values() for p in prods if p[0] == "hotspot")
    n_pz = sum(1 for prods in producers.values() for p in prods if p[0] == "puzzle")
    rep.info("Nguon cap co tien trinh: %d khai bao grants_flag (%d tren hotspot + %d tren "
             "puzzle), cap cho %d co. Day la TOAN BO nguon cap - trinh kiem khong tu tong hop "
             "them mot ten co nao, khong theo quy uoc nao, khong suy luan tu id."
             % (n_hs + n_pz, n_hs, n_pz, len(producers)))

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


def check_item_consumption(ch: Chapter, rep: Report) -> None:
    """
    GIAI DOAN 9 - DOI CHIEU NGU NGHIA TIEU HAO VOI NHU CAU VE SAU.

    Mot hotspot USE_ITEM co consumes_item = true xoa han vat pham khoi tui do. Neu vat pham
    do con duoc doi o cho khac (required_item cua hotspot khac, required_items cua mot cau
    do, hoac required_items cua mot unlock_condition), nguoi choi co the tu tay khoa chinh
    minh ra ngoai phan con lai cua chuong - dung cai kieu soft-lock ma khong crash, khong
    log, khong ai biet cho den khi co nguoi chuyen phan nan.

    Phep kiem nay la phep kiem TINH (khong biet thu tu), nen no chi neu nghi van; ban chung
    minh that su la mo phong diem bat dong o GIAI DOAN 10 - o do consumes_item duoc thi hanh
    dung nhu engine se lam.
    """
    def needs_of(item, skip_hs, use_item_only=False):
        needs = []
        for h_id, (a_id, h) in sorted(ch.hotspots.items()):
            if h_id == skip_hs or h.get("required_item") != item:
                continue
            if use_item_only and h.get("action_type") != "USE_ITEM":
                continue
            needs.append("hotspot %s (%s, %s)" % (h_id, a_id, h.get("action_type")))
        if not use_item_only:
            for pz_id, (a_id, pz) in sorted(ch.puzzles.items()):
                if item in str_list(pz, "required_items"):
                    needs.append("cau do %s (%s)" % (pz_id, a_id))
            for a_id, uc in sorted(ch.unlock.items()):
                if item in uc["items"]:
                    needs.append("unlock_condition cua %s" % a_id)
        return needs

    n_use, n_consume, n_lock, n_declared = 0, 0, 0, 0
    for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
        if hs.get("action_type") != "USE_ITEM":
            continue
        n_use += 1
        if "consumes_item" in hs:
            n_declared += 1
        item = hs.get("required_item")
        if not is_str(item):
            continue
        where = "%s / %s" % (area_id, hs_id)

        if hs.get("consumes_item") is True:
            n_consume += 1
            needs = needs_of(item, hs_id)
            if needs:
                rep.warn(
                    where,
                    "\"consumes_item\": true xoa han '%s' khoi tui do, nhung %d cho khac van "
                    "doi vat pham nay: %s. Neu nguoi choi dung o day truoc, nhung cho kia ket "
                    "cung vinh vien." % (item, len(needs), fmt_list(needs, limit=4)),
                    "Hoac dat \"consumes_item\": false (kem \"locks_item\": true neu chi muon "
                    "cam dung lai), hoac cho hotspot nay trao lai mot vat pham thay the, hoac "
                    "doi thiet ke de nhung cho kia khong con can toi no.",
                )
        elif hs.get("locks_item") is True:
            n_lock += 1
            needs = needs_of(item, hs_id, use_item_only=True)
            if needs:
                rep.warn(
                    where,
                    "\"locks_item\": true giu '%s' lai trong tui nhung khoa khong cho keo-tha "
                    "nua, trong khi %s van can keo no len mot hotspot USE_ITEM."
                    % (item, fmt_list(needs, limit=4)),
                    "Dat \"locks_item\": false neu vat pham nay con phai dung tiep.",
                )

    if n_use and n_declared == n_use:
        rep.ok("Ngu nghia tieu hao doc duoc bang may o ca %d hotspot USE_ITEM: %d tieu huy vat "
               "pham (consumes_item=true), %d giu lai va khoa (locks_item=true), %d giu lai va "
               "dung lai tu do. Mo phong kha giai thi hanh dung nhung gia tri nay, khong gia "
               "dinh gi them." % (n_use, n_consume, n_lock, n_use - n_consume - n_lock))


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

    dead = 0          # [LOI] - chung minh duoc la khong bao gio ban
    nghi_ngo = 0      # [CANH BAO] - co dau hieu khong bao gio ban, chua chung minh duoc
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
                nghi_ngo += 1
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
                nghi_ngo += 1
                rep.warn(
                    where,
                    "Cu doa ON_WRONG_ITEM_USE tro toi '%s' nhung khong hotspot nao dung toi vat "
                    "pham do - kha nang cao no khong bao gio ban." % tii,
                )

    # PHAM VI THAT SU CUA PHEP KIEM NAY, noi cho dung:
    #   ON_COLLECT_ITEM      duoc chung minh den noi ([LOI] neu vat pham khong nhat duoc).
    #   ON_PUZZLE_FAIL_COUNT / ON_WRONG_ITEM_USE  chi soi duoc mot dau hieu -> [CANH BAO].
    #   ON_ENTER_AREA / ON_TIMER  KHONG duoc soi o day chut nao.
    # Ban truoc in "moi jumpscare deu co duong kich hoat co that" khi 'dead' = 0, ma 'dead'
    # chi dem rieng nhanh ON_COLLECT_ITEM - nen cau ay van duoc in ngay ben duoi mot
    # [CANH BAO] cua chinh no noi "no khong bao gio ban". Cau chu rong hon phep kiem.
    if not dead and not nghi_ngo:
        n_soi = sum(1 for _, (_, js) in ch.jumpscares.items()
                    if js.get("trigger_type") in ("ON_COLLECT_ITEM", "ON_PUZZLE_FAIL_COUNT",
                                                  "ON_WRONG_ITEM_USE"))
        rep.ok("Khong cu doa chet nao trong %d/%d cu doa ma giai doan nay soi duoc "
               "(ON_COLLECT_ITEM, ON_PUZZLE_FAIL_COUNT, ON_WRONG_ITEM_USE). "
               "ON_ENTER_AREA / ON_TIMER khong duoc soi o day."
               % (n_soi, len(ch.jumpscares)))
    elif not dead:
        rep.info("Khong cu doa chet nao o muc [LOI], nhung con %d cu doa bi danh dau "
                 "[CANH BAO] la co the khong bao gio ban - xem cac muc tren."
                 % nghi_ngo)


# --------------------------------------------------------------------------
# GIAI DOAN 10: KHA GIAI - THUAT TOAN DIEM BAT DONG
# --------------------------------------------------------------------------

def simulate_player(ch: Chapter, rep: Report, trace_enabled: bool = False):
    """
    Mo phong nguoi choi bang thuat toan diem bat dong (fixpoint / least fixed point).

    NGUON DU KIEN - va CHI nhung nguon nay, tat ca deu la GIA TRI doc thang tu JSON:
      * hotspot.required_item      vat pham phai co trong tui do
      * hotspot.required_flags     co tien trinh phai bat du (AND)
      * hotspot.grants_flag        co duoc bat khi hotspot chay xong
      * hotspot.consumes_item      dung xong vat pham co bi xoa khoi tui do khong
      * hotspot.locks_item         dung xong vat pham co bi khoa (khong dung lai duoc) khong
      * puzzle.required_items      dung cu phai cam moi nhap duoc loi giai
      * puzzle.grants_flag         co bat khi giai dung
      * puzzle.reward_item_id      phan thuong - GIAO THEO CAU TRUC, xem duoi
      * unlock_condition           dieu kien vao khu vuc trong chapter_01.json

    GIAO PHAN THUONG CAU DO: phan thuong chi roi thang vao tui do khi KHONG mot hotspot
    COLLECT_ITEM nao trong chuong khai "item_id" bang chinh no. Co hotspot giao hang thi
    phan thuong phai di qua hotspot ay va qua het cong required_flags cua no. Luat nay doc
    tu cau truc du lieu chu khong tu ten; bo no di la dung lai dung canh AO ma vong nay di
    go (xem ghi chu dai trong nhanh ZOOM_PUZZLE).

    KHONG CON MOT CANH NAO KHAC. Dac biet: mo phong nay KHONG tu cap co "flag_<puzzle_id>_
    solved" khi giai xong mot cau do. Cai luat do - tung mang nhan "quy uoc chinh tac" -
    dung TEN DINH DANH de dung ra mot ten co, chu khong doc mot truong nao trong du lieu;
    no la mot canh AO, va no tung lam trinh kiem in "[OK] KHA GIAI ... 5/5 khu vuc" cho mot
    ban du lieu da bi xoa mat nguon cap co, trong khi mo phong doc lap chi di duoc 3/5.
    Co chi den tu grants_flag. Muon cau do bat co thi ghi grants_flag vao cau do.

    Vong lap: moi vong quet toan bo hotspot cua nhung khu vuc DA toi duoc va lam moi viec
    lam duoc voi trang thai hien tai. Vong nao khong doi trang thai nua thi dung - do la
    diem bat dong, tuc toan bo phan nguoi choi co the voi toi.

    TIEU HAO VAT PHAM: khong con gia dinh nao ca. Mo phong TON TRONG truong consumes_item:
    dung xong mot hotspot USE_ITEM co consumes_item = true thi vat pham bi go khoi 'inventory'
    that. locks_item = true thi vat pham o lai trong tui (van tinh la "dang co" cho moi dieu
    kien) nhung khong keo-tha len mot hotspot USE_ITEM nao khac duoc nua.

    'ever_held' ghi lai moi vat pham nguoi choi TUNG cam - dung cho phep kiem "vat pham chet
    khong bao gio cham toi", vi mot vat pham bi tieu thu dung cach van la vat pham da cam.
    """
    reached = set()
    inventory = set()        # dang co trong tui do NGAY LUC NAY
    ever_held = set()        # tung cam, ke ca da bi tieu thu ve sau
    locked = set()           # o lai trong tui nhung khong keo-tha duoc nua (locks_item)
    solved = set()
    flags = set()
    fired = set()
    trace = []
    # item_id -> hotspot COLLECT_ITEM chiu trach nhiem dat no vao tui do (neu co).
    delivery = ch.item_delivery_hotspots()

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
        if is_str(req):
            if req not in inventory:
                miss_items.append(req)
            elif req in locked and hs.get("action_type") == "USE_ITEM":
                # Con nam trong tui, nhung da bi khoa boi mot hotspot USE_ITEM truoc do:
                # keo-tha khong con duoc nua, nen hotspot nay khong bao gio chay.
                miss_items.append("%s (dang bi khoa - locks_item)" % req)
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
                        ever_held.add(item_id)
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
                        ever_held.add(item_id)
                        trace.append((round_no, "VAT PHAM", item_id,
                                      "tao ra tai %s / %s" % (area_id, hs_id)))
                    grant_flag(hs.get("grants_flag"),
                               "%s / %s (dung %s)" % (area_id, hs_id, req), round_no)
                    # -- ngu nghia tieu hao: DOC TU DU LIEU, khong gia dinh ----
                    if hs.get("consumes_item") is True:
                        inventory.discard(req)
                        trace.append((round_no, "TIEU HAO", req,
                                      "bi xoa khoi tui do tai %s / %s (consumes_item=true)"
                                      % (area_id, hs_id)))
                    elif hs.get("locks_item") is True:
                        locked.add(req)
                        trace.append((round_no, "KHOA", req,
                                      "o lai trong tui nhung khoa tai %s / %s (locks_item=true)"
                                      % (area_id, hs_id)))

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
                    # KHONG co dong "grant_flag(\'flag_%s_solved\' % pz_id, ...)" o day nua:
                    # do la canh ao duy nhat con sot lai cua ban truoc. Co cua cau do chi den
                    # tu chinh truong grants_flag cua no.
                    grant_flag(pz.get("grants_flag"), "giai %s (grants_flag)" % pz_id, round_no)
                    grant_flag(hs.get("grants_flag"), "%s / %s" % (area_id, hs_id), round_no)
                    # -- GIAO PHAN THUONG: doc tu cau truc du lieu, khong gia dinh ----
                    #
                    # Ban truoc cong thang reward_item_id vao tui do NGAY khi giai xong, du
                    # trong chuong co mot hotspot COLLECT_ITEM rieng chiu trach nhiem giao
                    # vat pham ay. Do la mot canh AO: no dung ra mot duong vao tui do khong
                    # ton tai trong game, va no lam chet cong required_flags cua chinh
                    # hotspot giao hang. Hau qua do duoc: mot mo phong doc lap - co ton
                    # trong hotspot giao hang - GAY khi xoa grants_flag cua
                    # puz_rap_chu_the_menh / puz_ba_hoi_chin_tieng / puz_xep_anh_gia_pha,
                    # con trinh kiem nay thi khong, vi no da phat vat pham bang duong tat.
                    #
                    # Luat dung, va no doc duoc bang may: neu CO hotspot COLLECT_ITEM nao
                    # khai "item_id" = reward_item_id thi phan thuong CHI vao tui qua hotspot
                    # ay (va phai vuot cong cua hotspot ay). Khong hotspot nao giao thi cau
                    # do moi trao thang. Khop dung voi item_catalog[].hotspot_trao.
                    rid = pz.get("reward_item_id")
                    if is_str(rid) and rid not in inventory:
                        if delivery.get(rid):
                            trace.append((round_no, "PHAN THUONG", rid,
                                          "lo ra tai cho, vao tui qua %s"
                                          % fmt_list(delivery[rid])))
                        else:
                            inventory.add(rid)
                            ever_held.add(rid)
                            trace.append((round_no, "VAT PHAM", rid,
                                          "phan thuong cua %s (khong hotspot nao giao - "
                                          "trao thang)" % pz_id))

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
        "reached": reached, "inventory": inventory, "ever_held": ever_held,
        "locked": locked, "solved": solved,
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

    # DI TOI duoc khu vuc cuoi KHONG dong nghia voi KET duoc chuong. Co ket chuong doc
    # thang tu manifest ('chapter_complete_flag') - khong suy ra tu ten - va no phai thuc
    # su duoc bat trong mo phong.
    if is_str(ch.complete_flag) and ch.complete_flag not in flags:
        failed = True
        prods = ch.flag_producers.get(ch.complete_flag) or []
        if not prods:
            why = "khong mot hotspot hay puzzle nao khai \"grants_flag\": \"%s\"" % ch.complete_flag
        else:
            blocked = []
            for kind, oid, oarea, _how in prods:
                if kind == "hotspot" and oid in ch.hotspots:
                    mi, mf = gate_missing(ch.hotspots[oid][1])
                    blocked.append("%s (%s) can %s" % (oid, oarea, fmt_list(mi + mf)
                                                       if (mi or mf) else
                                                       "khu vuc chua toi duoc"
                                                       if oarea not in reached else "(khong ro)"))
                else:
                    blocked.append("%s '%s' (%s)%s" % (kind, oid, oarea,
                                                       "" if oid in solved else " - chua giai duoc"))
            why = "nguon cap bi chan: %s" % fmt_list(blocked)
        rep.error("kha giai / co ket chuong",
                  "Co ket chuong '%s' KHONG BAO GIO bat len duoc - nguoi choi co the di toi "
                  "khu vuc cuoi nhung khong hoan thanh duoc Chuong 1. %s"
                  % (ch.complete_flag, why),
                  "Mo duong toi hotspot/puzzle giu \"grants_flag\": \"%s\"." % ch.complete_flag)

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
        if item_id in ever_held:
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
    missing_rewards = sorted(r for r in reward_items if r not in ever_held)
    if missing_rewards:
        failed = True
        rep.error("kha giai / phan thuong",
                  "Khong lay duoc phan thuong cua cau do: %s." % fmt_list(missing_rewards))

    # ---- KET DUNG O DAU: in nguyen trang thai diem bat dong ----------------
    if failed:
        report_stop_point(ch, rep, result, gate_missing)
    else:
        n_consumed = len(ever_held) - len(inventory)
        rep.ok("KHA GIAI: dat diem bat dong sau %d vong lap, chi di tren nhung canh co that "
               "trong du lieu. Nguoi choi di duoc tu '%s' toi khu vuc ket chuong '%s'."
               % (round_no, start, final_area))
        rep.plain("Toi duoc %d/%d khu vuc  |  giai %d/%d cau do  |  cam %d/%d vat pham  |  "
                  "bat %d co tien trinh."
                  % (len(reached), len(ch.area_order), len(solved), len(ch.puzzles),
                     len(ever_held), len(ch.items), len(flags)))
        rep.plain("Ngu nghia tieu hao la THAT, khong phai gia dinh: mo phong doc consumes_item "
                  "cua tung hotspot USE_ITEM. Ket chuong voi %d vat pham da bi tieu thu %s "
                  "va %d vat pham bi khoa tai cho %s."
                  % (n_consumed,
                     ("(%s)" % fmt_list(sorted(ever_held - inventory))) if n_consumed else "",
                     len(locked),
                     ("(%s)" % fmt_list(sorted(locked))) if locked else ""))
        rep.plain("Khong mot co tien trinh nao duoc trinh kiem tu tong hop: tat ca %d co deu "
                  "den tu mot truong grants_flag co that trong JSON." % len(flags))

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
    ever_held = result.get("ever_held", inventory)
    locked = result.get("locked", set())
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
    rep.plain("  Vat pham TUNG cam (%d/%d): %s"
              % (len(ever_held), len(ch.items), fmt_list(sorted(ever_held), limit=12)))
    rep.plain("  Vat pham CON THIEU: %s"
              % fmt_list(sorted(i for i in ch.items if i not in ever_held), limit=12))
    rep.plain("  Con trong tui luc ket: %s  |  da tieu thu: %s  |  bi khoa tai cho: %s"
              % (fmt_list(sorted(inventory), limit=12) or "khong co",
                 fmt_list(sorted(ever_held - inventory), limit=12) or "khong co",
                 fmt_list(sorted(locked), limit=12) or "khong co"))
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

    # ---- CO TIEN TRINH MA LIVEOPS DOI ------------------------------------
    #
    # LiveOps chan cong ban hang bang co ("requires": {"flag": ...}). Neu co do khong ai
    # cap thi cong ay khoa VINH VIEN voi moi nguoi choi - mot loi khong lo ra trong bat ky
    # phep kiem nao cua rieng man choi, vi no nam vat ngang giua hai file du lieu.
    #
    # Mot co lien tai duoc chap nhan khi va chi khi no den tu MOT trong hai nguon doc duoc
    # bang may - khong suy dien tu ten:
    #   (1) Chuong 1 cap no  -> co mat trong flag_producers (grants_flag), tuc co that;
    #   (2) chinh file LiveOps nay cap no -> nam trong mot 'unlock.grants_flags' nao do
    #       (vd flag_chapter_02_unlocked do goi mua ban giao).
    # Rieng truong hop (1) con doi them: co phai duoc Chuong 1 khai la BAN GIAO
    # ('exported_flags' hoac 'chapter_complete_flag'), vi lop mua hang nam ngoai chuong va
    # chi duoc doc nhung gi chuong tuyen bo xuat ra.
    liveops_granted = set()
    for prod in (iap.get("products") or []) if is_dict(iap) else []:
        if not is_dict(prod):
            continue
        for f in ((prod.get("unlock") or {}).get("grants_flags") or []):
            if is_str(f):
                liveops_granted.add(f)

    chapter_exports = set(ch.exported_flags)
    if is_str(ch.complete_flag):
        chapter_exports.add(ch.complete_flag)

    for i, prod in enumerate((iap.get("products") or []) if is_dict(iap) else []):
        if not is_dict(prod):
            continue
        need = (prod.get("requires") or {}).get("flag")
        if not is_str(need):
            continue
        where = "%s / iap.products[%d] (%s)" % (W, i, prod.get("iap_product_id", "?"))
        if need in liveops_granted:
            continue
        if need in ch.flag_producers:
            if need not in chapter_exports:
                rep.error(where,
                          "Chan cong ban bang co '%s'. Chuong 1 CO cap co nay, nhung khong khai "
                          "no trong 'exported_flags' / 'chapter_complete_flag' - lop mua hang "
                          "nam ngoai chuong, no chi duoc doc nhung co chuong tuyen bo xuat ra."
                          % need,
                          "Them '%s' vao 'exported_flags' cua data/chapter_01.json." % need)
            continue
        rep.error(where,
                  "Chan cong ban bang co '%s', nhung KHONG dau cap no: khong mot hotspot hay "
                  "cau do nao cua Chuong 1 khai \"grants_flag\": \"%s\", va cung khong goi IAP "
                  "nao trong chinh file nay cap no qua 'unlock.grants_flags'. Cong ban khoa "
                  "VINH VIEN voi moi nguoi choi. Co ket chuong that cua Chuong 1 la '%s'."
                  % (need, need, ch.complete_flag or "(chua khai chapter_complete_flag)"),
                  "Tro 'requires.flag' toi dung co ket chuong, hoac them nguon cap cho co nay.")

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
        # Ban truoc in "trinh kiem nay hien thuc toan bo 16 bat bien goc" ngay canh
        # len(invariants) - mot con so GHI CUNG dung lam loi cam ket. Them mot bat bien vao
        # file cau hinh ma quen hien thuc no thi cau ay tu dong thanh loi khai man, va khong
        # lop nao bat duoc. Gio hai con so duoc DOI CHIEU voi nhau.
        n_declared = len(invariants)
        if n_declared != N_LIVEOPS_INVARIANTS_IMPLEMENTED:
            rep.error(W,
                      "File cau hinh khai bao %d bat bien nhung trinh kiem moi hien thuc %d. "
                      "Bat bien khai ma khong ai kiem la bat bien khong ton tai."
                      % (n_declared, N_LIVEOPS_INVARIANTS_IMPLEMENTED),
                      "Hien thuc not trong check_liveops() roi tang "
                      "N_LIVEOPS_INVARIANTS_IMPLEMENTED, hoac bo dong khai bao thua.")
        else:
            # Phep kiem nay doi chieu HAI CON SO, khong doi chieu NOI DUNG. No khong the
            # ket luan "dung nhung bat bien do" - doi ten hoac thay hang mot dong trong
            # 'invariants' ma van giu so luong thi no khong thay gi. Cau chu phai dung
            # bang pham vi ay.
            rep.info("File cau hinh khai bao %d bat bien va trinh kiem hien thuc %d - HAI "
                     "CON SO KHOP. So thu hai duoc sinh ra bang len(LIVEOPS_INVARIANTS_"
                     "IMPLEMENTED), nhung DANH SACH ay do nguoi viet duy tri bang tay. "
                     "Va day la phep dem, khong phai phep doi chieu tung bat bien: viec tung "
                     "dong trong 'invariants' co ung voi dung phep kiem nao khong van phai "
                     "ra soat tay."
                     % (n_declared, N_LIVEOPS_INVARIANTS_IMPLEMENTED))


# --------------------------------------------------------------------------
# DIEU PHOI
# --------------------------------------------------------------------------

def read_level_files(args, rep: Report):
    """
    GIAI DOAN 1 - doc va phan tich JSON tu dia.

    Tach rieng khoi build_chapter()/check_level() vi che do --self-test can chay lai TOAN BO
    phep kiem tren nhung ban sao da bi dot bien TRONG BO NHO, khong duoc ghi ra dia.

    Tra ve (manifest, areas_raw) - hoac (None, None) neu khong doc noi manifest.
    """
    data_dir = os.path.abspath(args.data_dir)
    manifest_path = args.manifest or os.path.join(data_dir, "chapter_01.json")
    areas_dir = os.path.join(data_dir, "areas")

    rep.section("GIAI DOAN 1 - DOC & PHAN TICH JSON")

    # In RO cay thu muc dang bi kiem, va no den tu dau. Che do that bai nguy hiem nhat cua
    # ban truoc la kiem nham cay ma khong ai biet: duong dan mac dinh go cung tro ve mot
    # thu muc tuyet doi, nen chay tu ban sao van ra ket luan cua ban goc.
    rep.info("Thu muc data dang kiem: %s" % data_dir)
    if args.data_dir == DEFAULT_DATA_DIR:
        rep.plain("(mac dinh, suy ra tu vi tri script: %s -> ../data)" % SCRIPT_DIR)
    else:
        rep.plain("(do nguoi dung truyen tren dong lenh)")
    if not os.path.isdir(data_dir):
        rep.error("data_dir", "Khong co thu muc data tai: %s" % data_dir,
                  "Truyen duong dan thu muc data dung tren dong lenh, vi du "
                  "'python3 tools/validate_level.py /duong/dan/data'.")
        return None, None

    manifest = load_json(manifest_path, rep, "chapter_01.json")
    if manifest is None:
        return None, None
    rep.ok("Doc duoc manifest chuong: %s" % manifest_path)

    if not is_dict(manifest):
        rep.error("chapter_01.json", "Manifest phai la mot doi tuong JSON o cap cao nhat.")
        return None, None

    area_order = [a for a in (manifest.get("area_order") or []) if is_str(a)]
    manifest_areas = {}
    for entry in (manifest.get("areas") or []):
        if is_dict(entry) and is_str(entry.get("area_id")):
            manifest_areas[entry["area_id"]] = entry

    areas_raw = {}
    for area_id in area_order:
        entry = manifest_areas.get(area_id)
        rel = (entry or {}).get("file") or os.path.join("areas", area_id + ".json")
        path = os.path.join(data_dir, rel) if not os.path.isabs(rel) else rel
        area = load_json(path, rep, "%s (%s)" % (area_id, rel))
        if area is None:
            continue
        if not is_dict(area):
            rep.error(area_id, "File area phai la mot doi tuong JSON o cap cao nhat.")
            continue
        areas_raw[area_id] = area

    if os.path.isdir(areas_dir):
        for name in sorted(os.listdir(areas_dir)):
            if not name.endswith(".json"):
                continue
            stem = name[:-5]
            if stem not in areas_raw:
                rep.warn("areas/%s" % name,
                         "File khu vuc nay khong duoc manifest tham chieu - se khong bao gio "
                         "duoc nap, va khong duoc kiem.",
                         "Them '%s' vao 'area_order' va 'areas' cua chapter_01.json, hoac xoa "
                         "file neu da bo." % stem)

    if areas_raw:
        rep.ok("Doc duoc %d/%d file khu vuc." % (len(areas_raw), len(area_order)))
    return manifest, areas_raw


def build_chapter(manifest, areas_raw, rep: Report) -> Chapter:
    """Dung doi tuong Chapter tu cac doi tuong JSON DA NAP (khong dung toi dia)."""
    ch = Chapter()
    ch.manifest = manifest if is_dict(manifest) else {}
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

    # 'chapter_complete_flag' (BAT BUOC): co ket chuong, khai bao TUONG MINH. Trinh kiem
    # tuyet doi khong duoc dung ra ten nay tu chapter_id hay tu ten hotspot - do dung la
    # kieu suy dien tu ten ma vong nay di go. Khong co truong nay thi GIAI DOAN 10 khong co
    # gi de doi chieu, va "toi duoc khu vuc cuoi" bi nham voi "hoan thanh duoc chuong".
    raw_complete = manifest.get("chapter_complete_flag")
    if raw_complete is None:
        rep.error("chapter_01.json",
                  "Thieu truong bat buoc 'chapter_complete_flag' - khong co co ket chuong thi "
                  "mo phong kha giai khong chung minh duoc nguoi choi KET duoc Chuong 1, no "
                  "chi chung minh duoc nguoi choi DI TOI duoc khu vuc cuoi.",
                  "Them \"chapter_complete_flag\": \"<flag_id>\" o cap cao nhat, tro toi dung "
                  "co ma hotspot/puzzle ket chuong khai trong 'grants_flag'.")
    elif not is_str(raw_complete) or not raw_complete.startswith(PREFIX["flag"]):
        rep.error("chapter_01.json",
                  "'chapter_complete_flag' = %r khong hop le - phai la chuoi bat dau bang '%s'."
                  % (raw_complete, PREFIX["flag"]))
    else:
        ch.complete_flag = raw_complete

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
        area = areas_raw.get(area_id)
        if area is None:
            continue
        ch.areas[area_id] = area
        ch.unlock[area_id] = normalize_unlock(
            (manifest_areas.get(area_id) or {}).get("unlock_condition"), area_id, rep)

    for area_id in sorted(manifest_areas):
        if area_id not in ch.area_order:
            rep.error("chapter_01.json", "Khu vuc '%s' khai bao trong 'areas' nhung khong co "
                                         "trong 'area_order' - se khong bao gio duoc nap." % area_id)
    return ch


def check_level(ch: Chapter, rep: Report, trace: bool = False) -> None:
    """GIAI DOAN 2 den 10 - toan bo phep kiem du lieu man choi tren mot Chapter da dung."""
    # ---- GIAI DOAN 2-4: cau truc + rang buoc co dieu kien + hinh hoc -------
    rep.section("GIAI DOAN 2-4 - CAU TRUC, RANG BUOC THEO LOAI, HINH HOC 1920x1080")
    n_err_before = len(rep.errors)
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

    if ch.areas and len(rep.errors) == n_err_before:
        # Vong lap tren chi di qua ch.area_order. File khu vuc khong duoc manifest tham
        # chieu KHONG duoc kiem o day (chi co mot [CANH BAO] rieng luc doc file), nen cau
        # chu phai noi dung pham vi da duyet thay vi "moi hotspot" chung chung.
        rep.ok("Trong %d khu vuc cua 'area_order': moi hotspot / puzzle / jumpscare deu du "
               "KHOA MASTER FORM, dung enum va nam tron trong khung %dx%d."
               % (len(ch.area_order), DESIGN_WIDTH, DESIGN_HEIGHT))

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
    rep.section("GIAI DOAN 7a - NGUON CAP CO TIEN TRINH (CHI TU TRUONG grants_flag)")
    build_flag_producers(ch, rep)
    if ch.flag_producers:
        rep.ok("Xac dinh duoc nguon cap cho %d co tien trinh." % len(ch.flag_producers))

    # ---- GIAI DOAN 7: tham chieu cheo -------------------------------------
    rep.section("GIAI DOAN 7b - THAM CHIEU CHEO")
    check_cross_references(ch, rep)

    # ---- GIAI DOAN 7c: doi chieu guong ------------------------------------
    rep.section("GIAI DOAN 7c - DOI CHIEU GUONG: MANIFEST vs FILE KHU VUC")
    check_manifest_mirror(ch, rep)

    # ---- GIAI DOAN 8: chu trinh -------------------------------------------
    rep.section("GIAI DOAN 8 - CHU TRINH TRONG DO THI PHU THUOC VAT PHAM")
    check_item_cycles(ch, rep)

    # ---- GIAI DOAN 9: vat pham chet ---------------------------------------
    rep.section("GIAI DOAN 9 - VAT PHAM CHET / TIEU HAO / CU DOA CHET")
    check_dead_items(ch, rep)
    check_item_consumption(ch, rep)
    check_dead_jumpscares(ch, rep)

    # ---- GIAI DOAN 10: kha giai -------------------------------------------
    rep.section("GIAI DOAN 10 - KHA GIAI (MO PHONG DIEM BAT DONG)")
    if ch.areas:
        simulate_player(ch, rep, trace_enabled=trace)
    else:
        rep.error("kha giai", "Khong nap duoc khu vuc nao - bo qua buoc chung minh kha giai.")


# --------------------------------------------------------------------------
# CHE DO TU KIEM DOT BIEN (--self-test)
# --------------------------------------------------------------------------
#
# Vong 2 sua nhan ("suy luan" -> "quy uoc chinh tac") ma khong go canh ao ra khoi mo phong,
# va khong ai phat hien duoc vi khong co phep thu nao BUOC trinh kiem phai chung minh rang
# no that su doc truong minh khai la doc. Day la phep thu do.
#
# Nguyen ly: neu trinh kiem thuc su doc truong X thi XOA X di phai lam no bao loi. Neu xoa X
# ma no van bao "sach hoan toan", thi ket luan cua no khong dua tren X - du tai lieu co viet
# gi di nua.

# Nhung giai doan duoc tinh la PHAT HIEN THAT SU. Co y KHONG tinh giai doan 2-4: o do
# grants_flag chi bi kiem SU CO MAT (kiem hinh thuc), va mot trinh kiem chi biet "truong nay
# phai co" van co the hoan toan mu ve Y NGHIA cua no. Chi khi lop suy luan tien trinh
# (7a) hoac mo phong kha giai (10) gay ra loi thi moi chac trinh kiem DUNG gia tri do.
SELF_TEST_LOGIC_SECTIONS = (
    ("GIAI DOAN 7a", "7a nguon cap co"),
    ("GIAI DOAN 10", "10 kha giai"),
)

# HO DOT BIEN THU HAI: ban sao trong manifest.
#
# puzzle_index / jumpscare_index / flag_registry / areas[].background_asset_url / area_files
# deu CHEP LAI gia tri von thuoc ve data/areas/*.json. Truoc ban nay khong ham nao doc chung,
# nen mot ban sao lech khong lop nao bat duoc - dung kieu loi "con so chep qua lai giua cac
# file ma khong ai dem lai tu nguon". Phep thu: lam lech mot ban sao, va doi phep doi chieu
# guong (GIAI DOAN 7c) phai bao loi. Chi tinh la phat hien khi loi den tu 7c: mot loi o giai
# doan khac nghia la dot bien ay bi bat NHO MOT LY DO KHAC, khong chung minh duoc rang ban
# sao dang duoc doi chieu.
SELF_TEST_MIRROR_SECTIONS = (
    ("GIAI DOAN 7c", "7c doi chieu guong"),
)

# HAI TOAN TU DOT BIEN, va ly do phai co ca hai.
#
# Vong 5 chi co MOT toan tu: doi gia tri (mutate_value). Mot toan tu chi biet doi gia tri
# thi chi tham do duoc nhung khoa DANG CO MAT, nen no mu hoan toan truoc lop lo hong "khoa
# vang mat khong ai gac" - va vi mu nen no van in "DAT (100%)". Ban tu kiem ay tu bao cao
# rong hon nhung gi no thuc su tham do, dung kieu loi ma no sinh ra de bat.
#
# Tu ban nay co hai toan tu, dem va bao cao TACH RIENG:
#   DOI GIA TRI  doi gia tri cua mot khoa dang co -> ban sao lech
#   XOA KHOA     xoa han mot khoa -> ban sao khuyet
# Thoat 0 chi khi CA HAI loai deu dat 100%. Mot loai dat 100%% khong noi gi ve loai kia.
OP_VALUE = "DOI GIA TRI"
OP_DELETE = "XOA KHOA"


def _clone(obj):
    """Ban sao sau, chi qua json - khong dung copy.deepcopy de giu dung ngu nghia du lieu."""
    return json.loads(json.dumps(obj))


def collect_grants_flag_points(ch: Chapter):
    """Moi diem co the dot bien: (loai, id, area_id, ten co dang khai bao)."""
    points = []
    for pz_id, (area_id, pz) in sorted(ch.puzzles.items()):
        if is_str(pz.get("grants_flag")):
            points.append(("puzzle", pz_id, area_id, pz["grants_flag"]))
    for hs_id, (area_id, hs) in sorted(ch.hotspots.items()):
        if is_str(hs.get("grants_flag")):
            points.append(("hotspot", hs_id, area_id, hs["grants_flag"]))
    return points


def run_one_mutation(manifest, areas_raw, kind: str, target_id: str):
    """
    Xoa grants_flag cua mot puzzle/hotspot TRONG BO NHO roi chay lai toan bo phep kiem.

    Tra ve (da_xoa_duoc, report). Report chay im lang, khong mau, khong --strict: chi
    nhung [LOI] that su moi duoc tinh la phat hien.
    """
    man2 = _clone(manifest)
    areas2 = dict((k, _clone(v)) for k, v in areas_raw.items())

    coll = "puzzles" if kind == "puzzle" else "hotspots"
    removed = False
    for area in areas2.values():
        for entry in (area.get(coll) or []):
            if is_dict(entry) and entry.get("id") == target_id and "grants_flag" in entry:
                entry.pop("grants_flag")
                removed = True

    rep = Report(Palette(False), quiet=True, strict=False)
    rep.section("GIAI DOAN 1 - DOC & PHAN TICH JSON")
    ch = build_chapter(man2, areas2, rep)
    check_level(ch, rep, trace=False)
    return removed, rep


def mutate_value(v):
    """Doi mot gia tri JSON thanh mot gia tri KHAC HAN cung muc dich - de doi chieu phai lech."""
    if isinstance(v, bool):
        return not v
    if isinstance(v, (int, float)):
        return v + 1
    if is_str(v):
        return v + "_DOT_BIEN"
    if v is None:
        return "DOT_BIEN"
    if is_list(v):
        return list(v) + ["DOT_BIEN"]
    return "DOT_BIEN"


def collect_manifest_mirror_points(manifest):
    """
    Moi GIA TRI ma manifest chep lai tu file khu vuc = mot diem co the dot bien.

    Danh sach nay duoc SINH RA tu chinh manifest dang nap, khong go tay: them mot muc vao
    puzzle_index thi so diem dot bien tu tang theo.
    """
    points = []

    def add(block, idx, key, label):
        points.append({"block": block, "idx": idx, "key": key, "label": label})

    for block_key, mirror in (("puzzle_index", PUZZLE_INDEX_MIRROR),
                              ("jumpscare_index", JUMPSCARE_INDEX_MIRROR)):
        for idx, entry in enumerate(manifest.get(block_key) or []):
            if not is_dict(entry):
                continue
            for key in sorted(entry):
                if key in mirror:
                    add(block_key, idx, key, "%s[%d].%s" % (block_key, idx, key))

    for idx, entry in enumerate(manifest.get("flag_registry") or []):
        if not is_dict(entry):
            continue
        for key in FLAG_REGISTRY_MIRROR:
            if key in entry:
                add("flag_registry", idx, key, "flag_registry[%d].%s" % (idx, key))

    for idx, entry in enumerate(manifest.get("areas") or []):
        if not is_dict(entry):
            continue
        for key in ("background_asset_url", "order"):
            if key in entry:
                add("areas", idx, key, "areas[%d].%s" % (idx, key))

    for idx, _val in enumerate(manifest.get("area_files") or []):
        add("area_files", idx, None, "area_files[%d]" % idx)

    return points


def run_one_mirror_mutation(manifest, areas_raw, point):
    """
    Sua MOT gia tri ban sao trong manifest (trong bo nho) roi chay lai toan bo phep kiem.

    Tra ve (da_sua_duoc, gia_tri_cu, gia_tri_moi, report).
    """
    man2 = _clone(manifest)
    areas2 = dict((k, _clone(v)) for k, v in areas_raw.items())

    block = man2.get(point["block"])
    old = new = None
    changed = False
    if is_list(block) and 0 <= point["idx"] < len(block):
        if point["key"] is None:
            old = block[point["idx"]]
            new = mutate_value(old)
            block[point["idx"]] = new
            changed = True
        else:
            entry = block[point["idx"]]
            if is_dict(entry) and point["key"] in entry:
                old = entry[point["key"]]
                new = mutate_value(old)
                entry[point["key"]] = new
                changed = True

    rep = Report(Palette(False), quiet=True, strict=False)
    rep.section("GIAI DOAN 1 - DOC & PHAN TICH JSON")
    ch = build_chapter(man2, areas2, rep)
    check_level(ch, rep, trace=False)
    return changed, old, new, rep


def collect_manifest_mirror_delete_points(manifest):
    """
    Moi KHOA guong co the XOA khoi manifest = mot diem dot bien cua toan tu XOA KHOA.

    Khac voi collect_manifest_mirror_points (toan tu doi gia tri), danh sach nay bo qua
    'area_files': cac muc o do la chuoi tran, khong co khoa nao de xoa - xoa mot muc la
    doi DO DAI mang, mot phep dot bien khac han va da co luat rieng gac.
    """
    points = []

    def add(block, idx, key):
        points.append({"block": block, "idx": idx, "key": key,
                       "label": "%s[%d].%s" % (block, idx, key)})

    for block_key, mirror in (("puzzle_index", PUZZLE_INDEX_MIRROR),
                              ("jumpscare_index", JUMPSCARE_INDEX_MIRROR)):
        for idx, entry in enumerate(manifest.get(block_key) or []):
            if not is_dict(entry):
                continue
            for key in sorted(entry):
                if key in mirror:
                    add(block_key, idx, key)

    for idx, entry in enumerate(manifest.get("flag_registry") or []):
        if not is_dict(entry):
            continue
        for key in FLAG_REGISTRY_MIRROR:
            if key in entry:
                add("flag_registry", idx, key)

    for idx, entry in enumerate(manifest.get("areas") or []):
        if not is_dict(entry):
            continue
        for key in ("background_asset_url", "order"):
            if key in entry:
                add("areas", idx, key)

    return points


def run_one_mirror_delete(manifest, areas_raw, point):
    """
    XOA HAN mot khoa ban sao trong manifest (trong bo nho) roi chay lai toan bo phep kiem.

    Tra ve (da_xoa_duoc, gia_tri_cu, report).
    """
    man2 = _clone(manifest)
    areas2 = dict((k, _clone(v)) for k, v in areas_raw.items())

    block = man2.get(point["block"])
    old = None
    removed = False
    if is_list(block) and 0 <= point["idx"] < len(block):
        entry = block[point["idx"]]
        if is_dict(entry) and point["key"] in entry:
            old = entry.pop(point["key"])
            removed = True

    rep = Report(Palette(False), quiet=True, strict=False)
    rep.section("GIAI DOAN 1 - DOC & PHAN TICH JSON")
    ch = build_chapter(man2, areas2, rep)
    check_level(ch, rep, trace=False)
    return removed, old, rep


def detected_sections(rep: Report, expected):
    """(danh sach giai doan co loi, cac giai doan MONG DOI that su co loi)."""
    sections = sorted(set(sec for _, _, sec in rep.errors))
    hit = [(pref, label) for pref, label in expected
           if any(sec.startswith(pref) for sec in sections)]
    return sections, hit


def run_self_test(args) -> int:
    use_color = sys.stdout.isatty() and not args.no_color and not os.environ.get("NO_COLOR")
    p = Palette(use_color)

    print(p.bold("=" * 78))
    print(p.bold("  TU KIEM DOT BIEN - trinh kiem co THAT SU doc nhung truong no khai khong?"))
    print(p.bold("=" * 78))
    print("  HAI TOAN TU DOT BIEN, dem va cham diem TACH RIENG:")
    print("    %s  doi gia tri cua mot khoa dang co mat  -> ban sao lech" % OP_VALUE)
    print("    %s     xoa han mot khoa                      -> ban sao khuyet" % OP_DELETE)
    print("  Ban truoc chi co toan tu %s. Mot toan tu chi biet doi gia tri chi tham do duoc"
          % OP_VALUE)
    print("  nhung khoa DANG CO MAT, nen no khong the nhin thay lop lo hong 'khoa vang mat")
    print("  khong ai gac' - va van in DAT (100%). Vi vay ty le phat hien duoi day duoc bao")
    print("  cao rieng cho tung toan tu, va ma thoat 0 doi CA HAI deu dat 100%.")
    print("")
    print("  HO A [%s] - grants_flag trong data/areas/*: voi moi puzzle va moi hotspot co"
          % OP_DELETE)
    print("  khai bao 'grants_flag', xoa truong do trong bo nho (KHONG ghi ra dia), chay lai")
    print("  toan bo phep kiem, va doi no phai BAO LOI. Chi tinh la phat hien khi loi den tu")
    print("  %s - day la nhung lop THAT SU dung gia tri cua truong, chu"
          % " hoac ".join(label for _, label in SELF_TEST_LOGIC_SECTIONS))
    print("  khong phai lop chi kiem xem truong co ton tai.")
    print("")
    print("  HO B1 [%s] - ban sao trong manifest: voi moi gia tri ma chapter_01.json"
          % OP_VALUE)
    print("  chep lai tu data/areas/* (puzzle_index, jumpscare_index, flag_registry,")
    print("  areas[].background_asset_url, areas[].order, area_files), SUA gia tri do va doi")
    print("  phep doi chieu guong (%s) phai BAO LOI."
          % ", ".join(label for _, label in SELF_TEST_MIRROR_SECTIONS))
    print("")
    print("  HO B2 [%s] - cung nhung ban sao ay, nhung XOA HAN khoa thay vi sua gia tri."
          % OP_DELETE)
    print("  Day la ho bao phu khoa guong grants_flag trong chapter_01.json, va la ho ma ban")
    print("  truoc khong co. Bo qua 'area_files': cac muc o do la chuoi tran, khong co khoa")
    print("  nao de xoa.")
    print("")

    base_rep = Report(Palette(False), quiet=True, strict=False)
    manifest, areas_raw = read_level_files(args, base_rep)
    if manifest is None:
        print(p.red("  [LOI] Khong doc duoc du lieu - khong the tu kiem."))
        return 1
    base_ch = build_chapter(manifest, areas_raw, base_rep)
    check_level(base_ch, base_rep, trace=False)

    if base_rep.errors:
        print(p.red("  [LOI] Du lieu GOC da co %d loi - phai sua het truoc khi tu kiem co "
                    "nghia." % len(base_rep.errors)))
        for where, msg, section in base_rep.errors[:10]:
            print("        - %s / %s: %s" % (section, where, msg[:110]))
        print("")
        print(p.bold("=" * 78))
        print("  %s" % p.red("TU KIEM KHONG CHAY DUOC - du lieu goc chua sach."))
        print(p.bold("=" * 78))
        return 1
    print("  %s Du lieu goc: 0 loi. Bat dau dot bien.\n" % p.green("[OK]"))

    # ---------------------------------------------------------------- HO A --
    points = collect_grants_flag_points(base_ch)
    if not points:
        print(p.red("  [LOI] Khong tim thay diem nao co 'grants_flag' de dot bien - "
                    "ban than dieu do da la mot loi du lieu."))
        return 1

    rows = []
    n_detected = 0
    for kind, target_id, area_id, flag in points:
        removed, rep = run_one_mutation(manifest, areas_raw, kind, target_id)
        sections, logic = detected_sections(rep, SELF_TEST_LOGIC_SECTIONS)
        ok = bool(removed) and bool(logic)
        if ok:
            n_detected += 1
        rows.append((kind, target_id, flag, removed, len(rep.errors), logic, ok))

        if not removed:
            print("  %s dot bien %s '%s': KHONG xoa duoc truong - diem nay khong ton tai "
                  "trong file area." % (p.red("[LOI]"), kind, target_id))
        elif not ok:
            print("  %s dot bien %s '%s' (xoa grants_flag = '%s'): trinh kiem VAN BAO SACH "
                  "o cac lop logic (%d loi, toan bo den tu %s)."
                  % (p.red("[LOI]"), kind, target_id, flag, len(rep.errors),
                     fmt_list(sections) or "khong lop nao"))
            print("        Day la bang chung trinh kiem KHONG doc gia tri cua truong nay: "
                  "ket luan kha giai cua no khong phu thuoc vao '%s'." % flag)

    print("")
    print(p.bold("  BANG KET QUA - HO A [%s]: XOA TRUONG grants_flag TRONG data/areas/*"
                 % OP_DELETE))
    print("  %-8s %-27s %-34s %-9s %s"
          % ("LOAI", "DINH DANH", "TRUONG grants_flag da xoa", "PHAT HIEN", "BOI GIAI DOAN"))
    print("  " + "-" * 92)
    for kind, target_id, flag, removed, n_err, logic, ok in rows:
        mark = p.green("%-9s" % "co") if ok else p.red("%-9s" % "KHONG")
        print("  %-8s %-27s %-34s %s %s"
              % (kind, target_id, flag, mark,
                 ("%s (%d loi)" % (" + ".join(lb for _, lb in logic), n_err))
                 if logic else "khong lop logic nao (%d loi)" % n_err))
    print("  " + "-" * 92)
    print("  Da dot bien %d diem  |  phat hien %d  |  bo sot %d"
          % (len(rows), n_detected, len(rows) - n_detected))

    # ---------------------------------------------------------------- HO B --
    mirror_points = collect_manifest_mirror_points(manifest)
    mirror_rows = []
    n_mirror_detected = 0
    if not mirror_points:
        print("")
        print("  %s Manifest khong co khoi ban sao nao (puzzle_index, jumpscare_index, "
              "flag_registry, area_files) de dot bien." % p.yellow("[CANH BAO]"))
    for point in mirror_points:
        changed, old, new, rep = run_one_mirror_mutation(manifest, areas_raw, point)
        sections, hit = detected_sections(rep, SELF_TEST_MIRROR_SECTIONS)
        ok = bool(changed) and bool(hit)
        if ok:
            n_mirror_detected += 1
        mirror_rows.append((point["label"], old, new, changed, len(rep.errors), hit, ok))

        if not changed:
            print("  %s dot bien '%s': KHONG sua duoc - diem nay khong ton tai trong manifest."
                  % (p.red("[LOI]"), point["label"]))
        elif not ok:
            print("  %s dot bien '%s' (%s -> %s): phep doi chieu guong VAN BAO SACH "
                  "(%d loi, den tu %s)."
                  % (p.red("[LOI]"), point["label"], json.dumps(old, ensure_ascii=False),
                     json.dumps(new, ensure_ascii=False), len(rep.errors),
                     fmt_list(sections) or "khong lop nao"))
            print("        Ban sao nay khong duoc doi chieu voi gia tri that: no co the lech "
                  "bao nhieu cung duoc ma khong lop nao bat.")

    if mirror_points:
        print("")
        print(p.bold("  BANG KET QUA - HO B1 [%s]: SUA GIA TRI BAN SAO TRONG MANIFEST"
                     % OP_VALUE))
        print("  %-44s %-32s %-9s %s"
              % ("GIA TRI BAN SAO DA SUA", "SUA THANH", "PHAT HIEN", "BOI GIAI DOAN"))
        print("  " + "-" * 104)
        for label, old, new, changed, n_err, hit, ok in mirror_rows:
            mark = p.green("%-9s" % "co") if ok else p.red("%-9s" % "KHONG")
            print("  %-44s %-32s %s %s"
                  % (label, json.dumps(new, ensure_ascii=False)[:32], mark,
                     ("%s (%d loi)" % (" + ".join(lb for _, lb in hit), n_err))
                     if hit else "khong lop doi chieu nao (%d loi)" % n_err))
        print("  " + "-" * 104)
        print("  Da dot bien %d diem  |  phat hien %d  |  bo sot %d"
              % (len(mirror_rows), n_mirror_detected,
                 len(mirror_rows) - n_mirror_detected))

    # --------------------------------------------------------------- HO B2 --
    del_points = collect_manifest_mirror_delete_points(manifest)
    del_rows = []
    n_del_detected = 0
    if not del_points:
        print("")
        print("  %s Manifest khong co khoa guong nao de XOA." % p.yellow("[CANH BAO]"))
    for point in del_points:
        removed, old, rep = run_one_mirror_delete(manifest, areas_raw, point)
        sections, hit = detected_sections(rep, SELF_TEST_MIRROR_SECTIONS)
        ok = bool(removed) and bool(hit)
        if ok:
            n_del_detected += 1
        del_rows.append((point["label"], old, removed, len(rep.errors), hit, ok))

        if not removed:
            print("  %s xoa khoa '%s': KHONG xoa duoc - khoa nay khong ton tai trong manifest."
                  % (p.red("[LOI]"), point["label"]))
        elif not ok:
            print("  %s XOA HAN khoa '%s' (gia tri cu %s): phep doi chieu guong VAN BAO SACH "
                  "(%d loi, den tu %s)."
                  % (p.red("[LOI]"), point["label"],
                     json.dumps(old, ensure_ascii=False), len(rep.errors),
                     fmt_list(sections) or "khong lop nao"))
            print("        Ban sao nay chi duoc gac MOT CHIEU: lech gia tri thi bat, nhung "
                  "khuyet han khoa thi lot. Xem luat duyet HOP o GIAI DOAN 7c.")

    if del_points:
        print("")
        print(p.bold("  BANG KET QUA - HO B2 [%s]: XOA HAN KHOA GUONG TRONG MANIFEST"
                     % OP_DELETE))
        print("  %-44s %-32s %-9s %s"
              % ("KHOA GUONG DA XOA", "GIA TRI CU", "PHAT HIEN", "BOI GIAI DOAN"))
        print("  " + "-" * 104)
        for label, old, removed, n_err, hit, ok in del_rows:
            mark = p.green("%-9s" % "co") if ok else p.red("%-9s" % "KHONG")
            print("  %-44s %-32s %s %s"
                  % (label, json.dumps(old, ensure_ascii=False)[:32], mark,
                     ("%s (%d loi)" % (" + ".join(lb for _, lb in hit), n_err))
                     if hit else "khong lop doi chieu nao (%d loi)" % n_err))
        print("  " + "-" * 104)
        print("  Da dot bien %d diem  |  phat hien %d  |  bo sot %d"
              % (len(del_rows), n_del_detected, len(del_rows) - n_del_detected))

    # ---------------------------------------------------------------- TONG --
    # Cham diem TACH RIENG theo TOAN TU. Gop chung hai loai lai thanh mot ty le duy nhat se
    # cho phep mot loai gan nhu mu van an theo diem cua loai kia - dung kieu tu bao cao rong
    # hon thuc te ma ban tu kiem nay sinh ra de chan.
    n_value = len(mirror_rows)
    n_value_ok = n_mirror_detected
    n_del = len(rows) + len(del_rows)
    n_del_ok = n_detected + n_del_detected

    def pct(ok, n):
        return "%.0f%%" % (100.0 * ok / n) if n else "n/a"

    print("")
    print(p.bold("=" * 78))
    print(p.bold("  TONG KET THEO TOAN TU"))
    print("  %-14s %-52s %-8s %-8s %s"
          % ("TOAN TU", "DIEM DOT BIEN", "SO DIEM", "BAT DUOC", "TY LE"))
    print("  " + "-" * 92)
    print("  %-14s %-52s %-8d %-8d %s"
          % (OP_VALUE, "ho B1: gia tri ban sao trong manifest",
             n_value, n_value_ok, pct(n_value_ok, n_value)))
    print("  %-14s %-52s %-8d %-8d %s"
          % (OP_DELETE, "ho A: %d truong grants_flag + ho B2: %d khoa guong"
             % (len(rows), len(del_rows)), n_del, n_del_ok, pct(n_del_ok, n_del)))
    print("  " + "-" * 92)

    total = n_value + n_del
    total_detected = n_value_ok + n_del_ok
    value_pass = bool(n_value) and n_value_ok == n_value
    del_pass = bool(n_del) and n_del_ok == n_del

    print("  TONG: %d diem dot bien  |  phat hien %d  |  bo sot %d"
          % (total, total_detected, total - total_detected))
    if value_pass and del_pass:
        print("  %s  Ca hai toan tu deu dat 100%%: %d diem %s va %d diem %s deu bi bat dung "
              "lop chiu trach nhiem."
              % (p.green("DAT"), n_value, OP_VALUE, n_del, OP_DELETE))
        print("        Pham vi cua ket luan nay dung bang pham vi da tham do: hai toan tu "
              "tren, tren nhung diem da liet ke o bang, khong hon.")
        print(p.bold("=" * 78))
        return 0
    for label, ok, n_ok, n_all in ((OP_VALUE, value_pass, n_value_ok, n_value),
                                   (OP_DELETE, del_pass, n_del_ok, n_del)):
        if not n_all:
            print("  %s  Toan tu %s khong co diem nao de dot bien - khong ket luan duoc gi "
                  "ve loai lo hong no phu trach." % (p.red("THAT BAI"), label))
        elif not ok:
            print("  %s  Toan tu %s: %d/%d diem KHONG bi phat hien. Trinh kiem dang ket luan "
                  "bang thu no khong doc."
                  % (p.red("THAT BAI"), label, n_all - n_ok, n_all))
    print(p.bold("=" * 78))
    return 1


# --------------------------------------------------------------------------
# DIEU PHOI
# --------------------------------------------------------------------------

def run(args) -> int:
    use_color = sys.stdout.isatty() and not args.no_color and not os.environ.get("NO_COLOR")
    palette = Palette(use_color)
    rep = Report(palette, quiet=args.quiet, strict=args.strict)

    data_dir = os.path.abspath(args.data_dir)

    manifest, areas_raw = read_level_files(args, rep)
    if manifest is None:
        rep.render("KIEM CHUNG DU LIEU MAN CHOI - LINH AN THON CHAPTER 1")
        return rep.render_summary(args.strict)

    ch = build_chapter(manifest, areas_raw, rep)
    check_level(ch, rep, trace=args.trace)

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
    parser.add_argument("--self-test", dest="self_test", action="store_true",
                        help="CHE DO TU KIEM DOT BIEN: hai toan tu - DOI GIA TRI (sua mot "
                             "khoa dang co) va XOA KHOA (xoa han mot khoa) - ap len truong "
                             "'grants_flag' va len moi ban sao manifest, trong bo nho, roi doi "
                             "trinh kiem phai BAO LOI. Ty le phat hien duoc bao cao RIENG cho "
                             "tung toan tu; thoat 0 chi khi CA HAI dat 100%%.")
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
        if args.self_test:
            return run_self_test(args)
        return run(args)
    except KeyboardInterrupt:
        print("\nDa dung theo yeu cau nguoi dung.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
