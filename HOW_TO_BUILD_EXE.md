# 如何在 Windows 上打包成 EXE 文件

由于开发环境限制，我们提供了这份简易指南，帮助您（或您的朋友）在 Windows 电脑上将此工具打包成 `.exe` 可执行文件。

## 第一步：准备环境

1.  **安装 Python**
    *   如果您还没有安装 Python，请访问 [python.org](https://www.python.org/downloads/) 下载并安装最新版。
    *   **重要**：安装时请务必勾选 **"Add Python to PATH"**（将 Python 添加到系统环境变量）。

2.  **打开命令提示符 (CMD) 或 PowerShell**
    *   在文件夹空白处按住 `Shift` + `右键`，选择“在此处打开 Powershell 窗口”或“在终端中打开”。

3.  **安装依赖库**
    *   在打开的窗口中输入以下命令并回车：
        ```bash
        pip install -r requirements.txt
        pip install pyinstaller
        ```
    *   等待安装完成。

## 第二步：打包成 EXE

继续在刚才的终端窗口中，输入以下命令并回车：

```bash
pyinstaller --noconsole --onefile --name="GIF转精灵图工具" gif_to_sprite_gui.py
```

**参数解释：**
*   `--noconsole`: 运行时不显示黑色的控制台窗口（适合图形界面程序）。
*   `--onefile`: 打包成单个 `.exe` 文件，方便发送。
*   `--name`:生成的 exe 文件名。

## 第三步：获取文件

*   命令运行完成后，您会看到一个名为 `dist` 的新文件夹。
*   打开 `dist` 文件夹，里面就会有一个 **`GIF转精灵图工具.exe`**。
*   您可以直接把这个 `.exe` 文件发给朋友，他们不需要安装 Python 就能运行了！

## 常见问题

*   **杀毒软件误报**：由于是个人打包的程序，没有数字签名，Windows Defender 或 360 可能会误报病毒。请选择“允许运行”或添加到信任列表。
*   **转换变慢**：打包成单文件后，启动速度可能会比直接运行脚本稍慢一点点，这是正常的。
