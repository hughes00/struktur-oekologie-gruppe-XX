Option Explicit
Dim fs, sh, root, python, candidates, candidate
Set fs = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
root = fs.GetParentFolderName(WScript.ScriptFullName)
candidates = Array(root & "\.venv\Scripts\pythonw.exe", sh.ExpandEnvironmentStrings("%USERPROFILE%") & "\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\pythonw.exe")
python = ""
For Each candidate In candidates
  If fs.FileExists(candidate) Then
    python = candidate
    Exit For
  End If
Next
If python = "" Then
  MsgBox "Python was not found automatically. Open this folder and run: python launch.pyw. See README.md.", 48, "Stockerau Carbon Atlas"
Else
  sh.CurrentDirectory = root
  sh.Run Chr(34) & python & Chr(34) & " -X utf8 " & Chr(34) & root & "\launch.pyw" & Chr(34), 0, False
End If
