import os, subprocess, sys, tkinter as tk
from tkinter import ttk, messagebox

# 延长子线程超时防止长时间调用被误认为卡死
import threading
threading.stack_size(0)  # 使用系统默认栈大小

# 智能路径检测
def get_tool_root():
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__ or "."))
    bag = os.path.join(base, "chino_bag")
    if os.path.isdir(bag):
        return bag
    return r"D:\u5de5\u5177"
TOOL_ROOT = get_tool_root()

# 工具描述（完整版）
TOOL_DESC = {
    # 处理器工具
    "CPUZ": "查看CPU型号/频率/缓存/主板信息",
    "CoreTemp": "实时监控CPU温度和功耗",
    "Prime95": "极限压力测试CPU稳定性",
    "LinX": "Linpack压力测试(比Prime95更热)",
    "ThrottleStop": "解锁CPU降频限制/降压调优",
    "wPrime": "多线程圆周率计算测CPU速度",
    "superpi": "单线程圆周率测单核性能",
    "C2CLatency": "测试CPU核心间延迟",
    "XIANGQI": "中国象棋基准跑分测试",
    # 显卡工具
    "GPUZ": "查看显卡型号/频率/显存/驱动版本",
    "DDU": "彻底清除显卡驱动残留(安全模式用)",
    "dxvachecker": "检查显卡支持的硬件解码格式",
    "GpuTest_Windows x64": "GeeXLab GPU压力测试(VULKAN/OpenGL)",
    "nvidiaInspector": "NVIDIA显卡频率/电压调节工具",
    "AMD显卡驱动下载": "跳转AMD官网下载最新驱动",
    "Nvidia显卡驱动下载": "跳转NVIDIA官网下载最新驱动",
    # 内存工具
    "MemTest64": "Windows下内存稳定性压力测试 (TechPowerUp出品)",
    "TestMem5": "DDR5/4 内存极限烤机 (anta777/Absolute配置)",
    "Thaiphoon": "读取内存SPD/XMP信息(台风)",
    "ZenTimings": "AMD平台内存时序查看",
    "ZenTimings_v1.39": "AMD平台内存时序查看 (v1.39)",
    "魔方内存盘": "用闲置内存创建虚拟硬盘",
    # 硬盘工具
    "7-zip": "硬盘顺序/随机读写速度测试",
    "ASSSDBenchmark": "SSD 4K对齐+读写速度测试",
    "CrystalDiskInfo": "硬盘健康状态(SMART)/温度/通电时间/读写量",
    "CrystalDiskMark": "硬盘顺序读写/随机4K速度基准测试 (Shizuku皮肤版)",
    "HDTune": "硬盘基准测试/坏道扫描",
    "DiskGenius": "磁盘分区管理/数据恢复",
    "DG6201829_x64": "DiskGenius 磁盘分区管理/数据恢复/备份",
    "PartitionGuru": "磁盘分区管理/数据恢复",
    "SpaceSniffer": "磁盘空间占用可视化分析",
    "WizTree": "极速磁盘空间分析(比Everything快)",
    # 烤鸡工具
    "FurMark": "FurMark 甜甜圈1(x86) — GPU压力测试",
    "FurMark_win64": "FurMark 2 甜甜圈2(x64 GUI) — GPU压力测试",
    "OCCT": "CPU+GPU+内存综合压力测试 (含温度/功耗监控)",
    "毒蘑菇测试": "网页端 GPU 压力测试 (WebGL Ray Marching, 热降频检测)",
    # 显示器工具
    "DisplayX": "显示器坏点/色彩/对比度测试",
    "monitorinfo": "显示器色域/面板信息检测",
    "UFO测试": "显示器刷新率/拖影测试(UFO Test)",
    "在线屏幕测试": "网页版显示器坏点/漏光检测",
    "色域检测": "显示器色域覆盖率检测",
    # 综合检测
    "hwinfo": "全硬件传感器实时监控(温度/电压/功耗)",
    "AIDA64": "系统全面信息检测+基准测试+稳定性验证",
    "HWMonitor": "CPUID HWMonitor温度/电压/频率监控",
    "speccy": "Piriform Speccy系统硬件信息一览",
    "CrystalMark Retro": "综合基准测试 (CPU/GPU/硬盘跑分) — Crystal Dew World 出品",
    "RWEverything": "底层硬件寄存器读写(高级调试)",
    # 外设工具
    "AresonMouseTest": "鼠标单击/双击/滚轮/轨迹检测",
    "Keyboard Test Utility": "键盘按键冲突/响应测试",
    "KeyTweak": "重新映射键盘键位(改键/宏)",
    "MOUSERATE": "测量鼠标USB回报率(Hz)",
    "MouseTester": "鼠标轨迹/加速度精准度测试",
    "在线外设测试中心": "网页版键盘/鼠标/手柄检测",
    "鼠标单机变双击测试器": "检测鼠标单击变双击问题",
    # 其他工具
    "DesktopOK": "保存/恢复桌面图标布局(多屏切换)",
    "DirectX_Repair": "修复DirectX/VC运行库缺失(缺DLL用)",
    "DirectX_Repair(Enhanced_Edition)": "DirectX增强版 — 修复DirectX/VC++运行库/C++组件",
    "MSIAfterburnerSetup": "MSI Afterburner超频/降压/监控",
    "next_itellyou": "MSDN原版Windows/Office镜像下载",
    "BatteryInfoView": "笔记本电池健康度/损耗率检测",
    "bluescreenview": "扫描蓝屏DMP文件/驱动堆栈/定位崩溃",
    "Dism++": "系统垃圾清理/WinSxS瘦身/启动项管理",
    "Everything": "极速全盘文件搜索(NTFS MFT读取)",
    "Geek Uninstaller": "彻底卸载软件+清理残留",
    "gifcam": "屏幕录制转GIF动图",
    "procexp": "高级进程管理器(比任务管理器强100倍)",
    "rufus": "制作可启动U盘(ISO写入)",
    "ULTRAISO": "镜像文件编辑/刻录/格式转换",
    "ventoy": "多系统U盘启动工具(N个ISO共存)",
    "WinDbg": "Windows高级调试工具(分析DMP/内核)",
    "天梯图": "CPU/显卡性能排行榜图片",
    "游戏加加": "游戏内帧率/温度/硬件监控OSD",
    "皮肤编辑器": "自定义软件皮肤/外观编辑器",
    "ATTODISKBENCHMARK": "硬盘读写速度测试(不同文件大小/队列深度)",
    "Defraggler": "硬盘碎片整理(可按文件/文件夹单独整理)",
    "FlashMaster": "U盘/闪存卡读写速度测试",
    "H2testw": "U盘/存储卡真实性容量检测(扩容盘检测)",
    "LLFTOOL": "硬盘低级格式化工具(彻底清零不可恢复)",
    "SSD utils": "SSD工具箱(固件升级/安全擦除/健康检测)",
    "SSDZ": "SSD信息检测(型号/主控/闪存颗粒/固件)",
    "TxBENCH": "SSD高级基准测试(随机读写/IOPS/延迟)",
    "URWTEST": "U盘/存储卡数据完整性验证(写满再读回)",
    "finaldata": "误删文件恢复/格式化后数据恢复工具",
    "mydisktest": "U盘/移动硬盘读写速度+数据完整性测试",
    "nvidiaProfileInspector": "NVIDIA驱动配置文件编辑器(高级调优)",
    "windirstat": "磁盘空间占用可视化(热力图大文件分析)",
    "魔方数据恢复": "误删文件/格式化/分区丢失数据恢复",
    # 游戏工具
    "battle": "暴雪战网客户端(魔兽/守望/暗黑/炉石)",
    "eaapp": "EA Play游戏客户端(战地/FIFA/APEX)",
    "epic": "Epic Games游戏平台(每周送免费游戏)",
    "GameBuff": "游戏加加加速器(帧率/延迟/优化)",
    "Steam": "Steam游戏平台(全球最大的PC游戏商店)",
    "雷神加速器": "雷神网游加速器",
    "迅游加速器": "迅游网游加速器",
    "迅雷加速器": "迅雷网游加速器",
    "斧牛加速器": "斧牛网游加速器",
    "玩家动力": "玩家动力游戏加速器",
    "风灵月影": "单机游戏修改器合集",
    # 2026/7/1 新增
    "7-Zip": "开源压缩解压工具 (7z/zip/rar) — https://7-zip.org",
    "AIO.NET.Offline": ".NET Framework 离线安装合集 (2.0-9.0) — 作者 Dragodraki",
    "VisualCppRedist_AIO": "VC++ 运行库全版本合集 (2005-2022) — 作者 abbodi1406",
    "PowerSettingsExplorer": "电源计划高级配置工具 (隐藏电源选项解锁)",
    "MSIAfterburnerSetup": "MSI Afterburner 显卡超频/降压/监控 — https://www.msi.com/Landing/afterburner",
}

# 分类 emoji
CAT_EMOJI = {
    "处理器工具": chr(0x1F532), "显卡工具": chr(0x1F3AE), "内存工具": chr(0x1F9EE),
    "硬盘工具": chr(0x1F4BE), "烤鸡工具": chr(0x1F525), "显示器工具": chr(0x1F5A5),
    "综合检测": chr(0x1F4CA), "外设工具": chr(0x1F5B1), "其他工具": chr(0x1F527),
    "游戏工具": chr(0x1F3AF),
}

# 扫描工具目录
def scan_tools():
    if not os.path.exists(TOOL_ROOT): return {}
    tools = {}
    for cat in os.listdir(TOOL_ROOT):
        cp = os.path.join(TOOL_ROOT, cat)
        if not os.path.isdir(cp): continue
        lst = []
        for tn in os.listdir(cp):
            tp = os.path.join(cp, tn)
            if not os.path.isdir(tp): continue
            exes = []
            for f in os.listdir(tp):
                fp = os.path.join(tp, f)
                if os.path.isfile(fp) and f.lower().endswith((".exe", ".url", ".bat")):
                    if not any(f.lower().startswith(s) for s in ('unins','unwi','remove')):
                        exes.append(fp)
            if exes:
                best = exes[0]
                for e in exes:
                    if tn.lower().replace(" ","") in os.path.splitext(os.path.basename(e))[0].lower():
                        best = e; break
                # 优先选择逻辑
                bn = tn.lower()
                if bn == '7-zip':
                    fm = [e for e in exes if os.path.basename(e).lower() == '7zfm.exe']
                    if fm: best = fm[0]
                if bn == 'crystaldiskmark':
                    s = [e for e in exes if os.path.basename(e).lower() == 'diskmark64a.exe']
                    if s: best = s[0]
                if bn == "furmark_win64":
                    g = [e for e in exes if "gui" in os.path.basename(e).lower()]
                    if g: best = g[0]
                if bn in ("dism++", "hwinfo", "bluescreenview"):
                    x64 = [e for e in exes if "64" in os.path.basename(e).lower() and "arm" not in os.path.basename(e).lower()]
                    if x64: best = x64[0]
                # GpuTest → 选 GUI 版
                if "gputest" in bn:
                    gui = [e for e in exes if "gui" in os.path.basename(e).lower()]
                    if gui: best = gui[0]
                # DiskGenius → 选 DiskGenius.exe
                if bn.startswith("dg") or "diskgenius" in bn or "partitionguru" in bn:
                    dg = [e for e in exes if "diskgenius.exe" == os.path.basename(e).lower()]
                    if dg: best = dg[0]
                # 32/64 双版本
                has32 = any("32" in os.path.basename(e).lower() for e in exes)
                has64 = any("64" in os.path.basename(e).lower() for e in exes)
                if has32 and has64:
                    x64_exe = next((e for e in exes if "64" in os.path.basename(e).lower()), None)
                    x86_exe = next((e for e in exes if "32" in os.path.basename(e).lower()), None)
                    if x64_exe and x86_exe:
                        lst.append((f"{tn} (64位)", x64_exe, TOOL_DESC.get(tn, "")))
                        lst.append((f"{tn} (32位)", x86_exe, TOOL_DESC.get(tn, "")))
                        continue
                d = TOOL_DESC.get(tn, "等待补充说明")
                lst.append((tn, best, d))
        if lst: tools[cat] = lst
    return tools

# 启动工具
def launch_tool(exe_path):
    TOOLS_NEED_ADMIN = ["cpuz", "gpu-z", "aida64", "hwinfo", "ddu", "diskgenius"]
    try:
        need_admin = any(kw in exe_path.lower() for kw in TOOLS_NEED_ADMIN)
        import ctypes as _ct
        verb = "runas" if need_admin else "open"
        _ct.windll.shell32.ShellExecuteW(None, verb, exe_path, None,
                                         os.path.dirname(os.path.abspath(exe_path)), 1)
    except Exception as e: messagebox.showerror("启动失败", str(e))


# 硬件信息获取 — 单次 PowerShell 调用，返回完整字典
# 显卡显存改为用 dxdiag 获取（CIM AdapterRAM 32位截断无法正确读取 16GB 显存）
def get_hardware_info():
    ps_script = r"""
$cpu = Get-CimInstance Win32_Processor | Select Name,NumberOfCores,ThreadCount,MaxClockSpeed | ConvertTo-Json -Compress
$board = Get-CimInstance Win32_BaseBoard | Select Manufacturer,Product | ConvertTo-Json -Compress
$bios = Get-CimInstance Win32_BIOS | Select SMBIOSBIOSVersion | ConvertTo-Json -Compress
$mem = Get-CimInstance Win32_PhysicalMemory | Select Capacity,Speed,Manufacturer,PartNumber,DeviceLocator | ConvertTo-Json -Compress
$gpu = Get-CimInstance Win32_VideoController | Where { $_.Name -notmatch 'Virtual' } | Select Name,DriverVersion | ConvertTo-Json -Compress
$disk = Get-CimInstance Win32_DiskDrive | Where { $_.Size -gt 0 } | Select Model,Size,InterfaceType | ConvertTo-Json -Compress
dxdiag /t "$env:TEMP\dxdiag_hw.txt" 2>$null | Out-Null
$vram=0;$monitor="";$mode="";$dxver="";$wddm=""
if (Test-Path "$env:TEMP\dxdiag_hw.txt") {
    $dx = Get-Content "$env:TEMP\dxdiag_hw.txt" -Raw
    if ($dx -match 'Dedicated Memory:\s*(\d+)\s*MB') { $vram = [int]$Matches[1] }
    if ($dx -match 'Monitor Model:\s*(.+)') { $monitor = $Matches[1].Trim() }
    if ($dx -match 'Current Mode:\s*(.+)') { $mode = $Matches[1].Trim() }
    if ($dx -match 'DirectX Version:\s*(.+)') { $dxver = $Matches[1].Trim() }
    if ($dx -match 'Driver Model:\s*(.+)') { $wddm = $Matches[1].Trim() }
}
Write-Output "CPU_JSON=$cpu"
Write-Output "BOARD_JSON=$board"
Write-Output "BIOS_JSON=$bios"
Write-Output "MEM_JSON=$mem"
Write-Output "GPU_JSON=$gpu"
Write-Output "DISK_JSON=$disk"
Write-Output "VRAM=$vram"
Write-Output "MONITOR=$monitor"
Write-Output "MODE=$mode"
Write-Output "DXVER=$dxver"
Write-Output "WDDM=$wddm"
"""
    import json as _json, re as _re
    info = {}
    try:
        si = subprocess.STARTUPINFO(); si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script],
                           capture_output=True, text=True, timeout=60,
                           startupinfo=si, creationflags=0x08000000)
        output = r.stdout

        def _get(key):
            m = _re.search(rf'{key}=(.*)', output)
            return m.group(1).strip() if m else ""

        cpu = _json.loads(_get("CPU_JSON")) if _get("CPU_JSON") else {}
        board = _json.loads(_get("BOARD_JSON")) if _get("BOARD_JSON") else {}
        bios = _json.loads(_get("BIOS_JSON")) if _get("BIOS_JSON") else {}
        mem_list = _json.loads(_get("MEM_JSON")) if _get("MEM_JSON") else []
        gpu_list = _json.loads(_get("GPU_JSON")) if _get("GPU_JSON") else []
        disk_list = _json.loads(_get("DISK_JSON")) if _get("DISK_JSON") else []
        vram_mb = int(_get("VRAM")) if _get("VRAM").isdigit() else 0
        monitor = _get("MONITOR")
        mode = _get("MODE")
        dxver = _get("DXVER")
        wddm = _get("WDDM")

        if not isinstance(mem_list, list): mem_list = [mem_list]
        if not isinstance(gpu_list, list): gpu_list = [gpu_list]
        if not isinstance(disk_list, list): disk_list = [disk_list]

        info["CPU"] = {
            "型号": cpu.get("Name", "N/A").strip() or "N/A",
            "核心数": f"{cpu.get('NumberOfCores',0)} 核 / {cpu.get('ThreadCount',0)} 线程",
            "最大频率": f"{cpu.get('MaxClockSpeed',0)} MHz",
        }
        info["主板"] = {
            "制造商": board.get("Manufacturer", "N/A"),
            "型号": board.get("Product", "N/A"),
            "BIOS": bios.get("SMBIOSBIOSVersion", "N/A"),
        }
        mem_total = 0; mem_detail = []
        for m in mem_list:
            cap = m.get("Capacity", 0) or 0; mem_total += cap
            mem_detail.append({
                "容量": f"{cap // (1024**3)} GB" if cap else "N/A",
                "频率": f"{m.get('Speed','')} MHz",
                "品牌": m.get("Manufacturer", "N/A"),
                "型号": m.get("PartNumber", "N/A"),
                "插槽": m.get("DeviceLocator", "N/A"),
            })
        if not mem_detail:
            mem_detail = [{"容量":"N/A","频率":"N/A","品牌":"N/A","型号":"N/A","插槽":"N/A"}]
        info["内存"] = {"总容量": f"{mem_total // (1024**3)} GB ({len(mem_detail)} 条)", "详细": mem_detail}
        gpu_detail = []
        for g in gpu_list:
            gpu_detail.append({
                "型号": g.get("Name", "N/A"),
                "显存": f"{round(vram_mb / 1024)} GB" if vram_mb else "N/A",
                "驱动版本": g.get("DriverVersion", "N/A"),
                "显示器": monitor if monitor else "",
                "分辨率": mode if mode else "",
                "DirectX": dxver if dxver else "",
                "WDDM": wddm if wddm else "",
            })
        if not gpu_detail:
            gpu_detail = [{"型号":"N/A","显存":"N/A","驱动版本":"N/A","显示器":"","分辨率":"","DirectX":"","WDDM":""}]
        info["显卡"] = gpu_detail
        disk_detail = []
        for d in disk_list:
            sz = d.get("Size", 0) or 0; gb = sz // (1000**3) if sz else 0
            disk_detail.append({
                "型号": d.get("Model", "N/A"),
                "容量": f"{gb} GB" if gb else "N/A",
                "接口": d.get("InterfaceType", "N/A"),
            })
        if not disk_detail:
            disk_detail = [{"型号":"N/A","容量":"N/A","接口":"N/A"}]
        info["硬盘"] = disk_detail
    except Exception as e:
        info["错误"] = str(e)
    return info


class ToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KafuuToolbox — 纯净硬件工具启动器")
        self.root.geometry("920x680")
        self.root.minsize(680, 500)
        self.root.configure(bg="#f5f2f0")

        # 显示模式: "desc" = 功能描述, "path" = 文件路径
        self.display_mode = tk.StringVar(value="desc")
        self.current_tool_list = []
        self._hw_cache = None

        # 顶栏
        top = tk.Frame(root, bg="#4f46e5", height=80)
        top.pack(fill=tk.X); top.pack_propagate(False)
        tk.Label(top, text="KafuuToolbox", font=("Microsoft YaHei",20,"bold"),
                 fg="white", bg="#4f46e5").pack(side=tk.LEFT, padx=20, pady=18)

        # 主区域
        panes = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 左侧分类列表
        lf = tk.Frame(panes, bg="#ffffff", width=190); lf.pack_propagate(False)
        panes.add(lf, weight=0)
        tk.Label(lf, text="工具分类", font=("Microsoft YaHei",11,"bold"),
                 fg="#4f46e5", bg="#ffffff").pack(fill=tk.X, padx=12, pady=(12,6))
        self.cats = tk.Listbox(lf, font=("Microsoft YaHei",11), selectmode=tk.SINGLE,
                               bg="#f9fafb", exportselection=False,
                               selectbackground="#e0e7ff", selectforeground="#4f46e5",
                               relief=tk.FLAT)
        self.cats.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        self.cats.bind("<<ListboxSelect>>", self.show_tools)

        # 右侧工具卡片区
        rf = tk.Frame(panes, bg="#f5f2f0"); panes.add(rf, weight=1)

        # 右侧顶栏: 分类标题 + 显示模式切换
        tr = tk.Frame(rf, bg="#f5f2f0")
        tr.pack(fill=tk.X, padx=12, pady=(8, 4))
        self.cat_label = tk.Label(tr, text="", font=("Microsoft YaHei",10),
                                  fg="#6b6b6b", bg="#f5f2f0", anchor=tk.W)
        self.cat_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 切换按钮
        sf = tk.Frame(tr, bg="#f5f2f0"); sf.pack(side=tk.RIGHT)
        self.btn_desc = tk.Button(sf, text="📝 用途", font=("Microsoft YaHei",9),
                                  relief=tk.FLAT, cursor="hand2",
                                  command=lambda: self.set_mode("desc"))
        self.btn_desc.pack(side=tk.LEFT, padx=(0,2))
        self.btn_path = tk.Button(sf, text="📁 路径", font=("Microsoft YaHei",9),
                                  relief=tk.FLAT, cursor="hand2",
                                  command=lambda: self.set_mode("path"))
        self.btn_path.pack(side=tk.LEFT)
        self._update_mode_buttons()

        # 工具卡片可滚动区
        self.hw_container = tk.Frame(rf, bg="#f5f2f0")
        self.canvas = tk.Canvas(rf, bg="#f5f2f0", highlightthickness=0)
        self.scroll = ttk.Scrollbar(rf, orient=tk.VERTICAL, command=self.canvas.yview)
        self.tool_frame = tk.Frame(self.canvas, bg="#f5f2f0")
        self.tool_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.tool_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1*(e.delta//120),"units"))

        # 底部状态栏
        self.status = tk.Label(root, text="就绪", font=("Microsoft YaHei",9),
                               fg="#9ca3af", bg="#f5f2f0")
        self.status.pack(fill=tk.X, padx=16, pady=(0,10))

        # 加载工具数据
        self.cats.insert(tk.END, "  🖥  硬件概览")
        self.tools = scan_tools()
        self.categories = sorted(self.tools.keys())
        for cat in self.categories:
            e = CAT_EMOJI.get(cat, chr(0x1F4E6))
            self.cats.insert(tk.END, f"  {e}  {cat}  ({len(self.tools[cat])})")
        if self.categories:
            self.cats.selection_set(0); self.show_tools(None)

    # 显示模式切换
    def set_mode(self, mode):
        self.display_mode.set(mode)
        self._update_mode_buttons()
        self._refresh_cards()

    def _update_mode_buttons(self):
        for btn, mode in [(self.btn_desc, "desc"), (self.btn_path, "path")]:
            if self.display_mode.get() == mode:
                btn.config(bg="#4f46e5", fg="white")
            else:
                btn.config(bg="#e5e0dc", fg="#6b6b6b")

    def _refresh_cards(self):
        """根据当前模式刷新所有卡片的描述文字"""
        mode = self.display_mode.get()
        for i, card_info in enumerate(self._card_widgets):
            _, exe, orig_desc = self.current_tool_list[i]
            if mode == "path":
                card_info["desc_label"].config(text=exe, font=("Consolas",8), fg="#9ca3af")
            else:
                card_info["desc_label"].config(text=orig_desc, font=("Microsoft YaHei",9), fg="#6b6b6b")

    # 显示工具列表
    def show_tools(self, event):
        sel = self.cats.curselection()
        if not sel: return
        if sel[0] == 0:  # 硬件概览
            self._show_hw_panel()
            return
        self._show_tools_panel()

        cat = self.categories[sel[0] - 1]  # 第0项是硬件概览，工具从索引1开始
        lst = self.tools.get(cat, [])
        self.current_tool_list = lst
        self.cat_label.config(text=cat)
        self._card_widgets = []


        self._hw_cache = None

        for w in self.tool_frame.winfo_children():
            w.destroy()

        cols = 2
        for i, (name, exe, desc) in enumerate(lst):
            card = tk.Frame(self.tool_frame, bg="white", relief=tk.RIDGE,
                            borderwidth=1, highlightbackground="#e5e0dc")
            card.grid(row=i//cols, column=i%cols, padx=8, pady=6, sticky="nsew")
            inn = tk.Frame(card, bg="white")
            inn.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

            tk.Label(inn, text=name, font=("Microsoft YaHei",13,"bold"),
                     fg="#1f2937", bg="white", anchor=tk.W).pack(fill=tk.X)

            # 描述标签（可切换）
            disp = desc if self.display_mode.get() == "desc" else exe
            dfont = ("Microsoft YaHei",9) if self.display_mode.get() == "desc" else ("Consolas",8)
            dcolor = "#6b6b6b" if self.display_mode.get() == "desc" else "#9ca3af"
            dl = tk.Label(inn, text=disp, font=dfont, fg=dcolor,
                          bg="white", anchor=tk.W, wraplength=280)
            dl.pack(fill=tk.X, pady=(3,8))

            tk.Button(inn, text="▶ 启动", font=("Microsoft YaHei",10,"bold"),
                      fg="white", bg="#4f46e5", relief=tk.FLAT, cursor="hand2",
                      padx=20, pady=4,
                      command=lambda p=exe, n=name: self.click(p,n)).pack(anchor=tk.W)

            self._card_widgets.append({"desc_label": dl})
            for cc in range(cols):
                self.tool_frame.columnconfigure(cc, weight=1, uniform="col")


# 硬件概览 UI 模块 — 追加到 ToolboxApp 类

    # ── 硬件概览面板 ──
    def _build_hw_panel(self, info):
        """根据硬件信息字典构建概览面板"""
        for w in self.hw_container.winfo_children():
            w.destroy()

        tk.Label(self.hw_container, text="🖥 硬件概览", font=("Microsoft YaHei",16,"bold"),
                 fg="#4f46e5", bg="#f5f2f0").pack(fill=tk.X, padx=20, pady=(16,4))

        hw_canvas = tk.Canvas(self.hw_container, bg="#f5f2f0", highlightthickness=0)
        hw_scroll = ttk.Scrollbar(self.hw_container, orient=tk.VERTICAL, command=hw_canvas.yview)
        hw_inner = tk.Frame(hw_canvas, bg="#f5f2f0")
        hw_inner.bind("<Configure>", lambda e: hw_canvas.configure(scrollregion=hw_canvas.bbox("all")))
        hw_canvas.create_window((0,0), window=hw_inner, anchor="nw")
        hw_canvas.configure(yscrollcommand=hw_scroll.set)
        hw_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        hw_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def _section(title, data, is_list=False):
            sec = tk.Frame(hw_inner, bg="white", relief=tk.RIDGE, borderwidth=1)
            tk.Label(sec, text=title, font=("Microsoft YaHei",12,"bold"), fg="#4f46e5", bg="white").pack(fill=tk.X, padx=14, pady=(10,4))
            sec.pack(fill=tk.X, padx=10, pady=6)
            if is_list:
                for item in data:
                    for key, val in list(item.items()):
                        if not val: continue
                        rf = tk.Frame(sec, bg="white"); rf.pack(fill=tk.X, padx=24, pady=1)
                        tk.Label(rf, text=f"{key}:", font=("Microsoft YaHei",9,"bold"), fg="#6b6b6b", bg="white", width=10).pack(side=tk.LEFT)
                        tk.Label(rf, text=val, font=("Microsoft YaHei",9), fg="#1f2937", bg="white", anchor=tk.W).pack(side=tk.LEFT, fill=tk.X)
            else:
                for key, val in data.items():
                    rf = tk.Frame(sec, bg="white"); rf.pack(fill=tk.X, padx=20, pady=2)
                    tk.Label(rf, text=f"{key}:", font=("Microsoft YaHei",9,"bold"), fg="#6b6b6b", bg="white", width=10).pack(side=tk.LEFT)
                    tk.Label(rf, text=val, font=("Microsoft YaHei",9), fg="#1f2937", bg="white", anchor=tk.W).pack(side=tk.LEFT, fill=tk.X)
            tk.Frame(sec, bg="#e5e0dc", height=1).pack(fill=tk.X, padx=14, pady=(6,0))

        _section("💻 CPU", info.get("CPU", {}))
        _section("📋 主板", info.get("主板", {}))
        _section("🧠 内存", info.get("内存", {}).get("详细", []), is_list=True)
        _section("🎮 显卡", info.get("显卡", []), is_list=True)
        _section("💾 硬盘", info.get("硬盘", []), is_list=True)

        tk.Button(hw_inner, text="🔄 刷新硬件信息", font=("Microsoft YaHei",10),
                  fg="white", bg="#4f46e5", relief=tk.FLAT, cursor="hand2", padx=20, pady=6,
                  command=lambda: (setattr(self, '_hw_cache', None), self._show_hw_panel())).pack(pady=12)

        self.status.config(text="就绪")

    def _show_hw_panel(self):
        """显示硬件概览面板（带进度条和缓存）"""
        self.canvas.pack_forget()
        self.scroll.pack_forget()
        self.hw_container.pack(fill=tk.BOTH, expand=True)
        if self._hw_cache is not None:
            self._build_hw_panel(self._hw_cache)
            return
        self.status.config(text="正在获取硬件信息...")
        loading = tk.Label(self.hw_container, text="    加载中，请稍候...", font=("Microsoft YaHei",12), fg="#9ca3af", bg="#f5f2f0")
        loading.pack(pady=60)
        pb = ttk.Progressbar(self.hw_container, mode="indeterminate", length=400)
        pb.pack(pady=10)
        pb.start(15)
        self.root.update()
        def _do_load():
            info = get_hardware_info()
            def _update_ui():
                pb.stop()
                pb.destroy()
                loading.destroy()
                self._hw_cache = info
                self._build_hw_panel(info)
            self.root.after(0, _update_ui)
        import threading
        threading.Thread(target=_do_load, daemon=True).start()

    def _show_tools_panel(self):
        """切换回工具卡片区"""
        self.hw_container.pack_forget()
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def click(self, exe, name):
        self.status.config(text=f"正在启动: {name}"); self.root.update()
        launch_tool(exe)
        self.status.config(text=f"已启动: {name}")

if __name__ == "__main__":
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas",
            sys.argv[0] if sys.argv[0] else sys.executable,
            " ".join(sys.argv[1:]), None, 1)
        sys.exit(0)
    root = tk.Tk()
    ToolboxApp(root)
    root.mainloop()
