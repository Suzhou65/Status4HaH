# -*- coding: utf-8 -*-
import status4hentai as s4h
from sys import exit
# Configuration file path
ConfigFilePath = "/Documents/script/status4hah.config.json"
# Script
def main():
    Rt = s4h.Runtime(ConfigFilePath)
    Eh = s4h.EHentai(ConfigFilePath)
    Al = s4h.Alert(ConfigFilePath)
    # Get Hentai@Home status
    ClientStatus = Eh.CheckHentaiatHome()
    # Error
    if isinstance(ClientStatus, bool):
        Rt.StatusRuntime("Error occurred during connect to E-hentai.")
        raise Exception()
    # E-Hentai server HTTP error
    elif isinstance(ClientStatus, int):
        Rt.StatusRuntime(f"E-Hentai Server Error: {ClientStatus}")
        raise Exception()
    # E-Hentai Logout
    elif isinstance(ClientStatus, str):
        Rt.StatusRuntime(ClientStatus)
        Al.Alarm(ClientStatus)
        raise Exception()
    # Get Hentai@Home status
    elif isinstance(ClientStatus, list):
        # Drop key
        Rt.StatusKeyDrop(ClientStatus)
        # Save web status
        Rt.StatusWebpage(ClientStatus)
    # Undefined error
    else:
        Rt.StatusRuntime(f"Undefined error occurred.")
        raise Exception()
    # Check online status
    OfflineClient = Eh.OfflineChecker(ClientStatus)
    if isinstance(OfflineClient, bool):
        Rt.StatusRuntime("Error occurred during check offline client.")
        raise Exception()
    elif isinstance(OfflineClient, list):
        if len(OfflineClient) == 0:
            Rt.StatusRuntime("All Hentai@Home client online.")
            # Delete continuous alert blocker
            Al.RemoveObstacle()
        else:
            Rt.StatusRuntime("Hentai@Home client offline detected.")
            OfflineNotify = (f"Hentai@Home client offline.\r\nClient Name: {OfflineClient}")
            Al.Alarm(OfflineNotify)
    # QC 2025L05
# Runtime
if __name__ == "__main__":
    try:
        main()
    except Exception:
        exit(0)
