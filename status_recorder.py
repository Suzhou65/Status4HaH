# -*- coding: utf-8 -*-
import status4hentai as s4h
from sys import exit

# Configuration file path
ConfigFilePath = "/Documents/script/status4hah.config.json"

def main():
    Rt = s4h.Runtime(ConfigFilePath)
    Eh = s4h.EHentai(ConfigFilePath)
    # Get Hentai@Home status
    ClientStatus = Eh.CheckHentaiatHome()
    # Error
    if isinstance(ClientStatus, bool):
        Rt.Message("Error occurred during connect to E-henati.")
        raise Exception()
    # E-Hentai server HTTP error
    elif isinstance(ClientStatus, int):
        Rt.Message(f"E-Hentai Server Error: {ClientStatus}")
        raise Exception()
    # E-Hentai Logout
    elif isinstance(ClientStatus, str):
        Rt.Message(ClientStatus)
        raise Exception()
    # Get Hentai@Home status
    elif isinstance(ClientStatus, list):
        # Drop key
        Rt.StatusKeyDrop(ClientStatus)
        # Writing into CSV file
        Rt.StatusRecorder(ClientStatus)
        Rt.Message("H@H clients status record successful.")
    # Undefined error
    else:
        Rt.Message(f"Undefined error occurred.")
        raise Exception()
    # QC 2025L04
# Runtime
if __name__ == "__main__":
    try:
        main()
    except Exception:
        exit(0)
