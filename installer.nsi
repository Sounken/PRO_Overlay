; PRO Helper Installer
; Simple NSIS installer without code signing

!include "MUI2.nsh"

; Basic Configuration
Name "PRO Helper v1.0.0"
OutFile "release\PROHelper-1.0.0-Setup.exe"
InstallDir "$PROGRAMFILES\PROHelper"
InstallDirRegKey HKCU "Software\PROHelper" "Install_Dir"

; MUI Settings
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "French"

; Installer sections
Section "Install"
  SetOutPath "$INSTDIR"
  File /r "frontend\release\win-unpacked\*.*"

  ; Create Start Menu shortcuts
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\PROHelper"
  CreateShortcut "$SMPROGRAMS\PROHelper\PRO Helper.lnk" "$INSTDIR\PROHelper.exe"
  CreateShortcut "$SMPROGRAMS\PROHelper\Uninstall.lnk" "$INSTDIR\uninstall.exe"

  ; Create Desktop shortcut
  CreateShortcut "$DESKTOP\PRO Helper.lnk" "$INSTDIR\PROHelper.exe"

  ; Write registry
  WriteRegStr HKCU "Software\PROHelper" "Install_Dir" "$INSTDIR"
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

; Uninstaller
Section "Uninstall"
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\PROHelper"
  Delete "$DESKTOP\PRO Helper.lnk"
  DeleteRegKey HKCU "Software\PROHelper"
SectionEnd
