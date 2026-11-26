#!/usr/bin/env python3
"""Integrity-only audit for archived PSP uClinux source bundles.

Never extracts files to disk, executes archive content, or prepares a console payload.
"""
from __future__ import annotations
import gzip, hashlib, json, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"platforms/linux-port-sources.json"
def main():
    data=json.loads(MANIFEST.read_text(encoding="utf-8"))
    source=next((x for x in data["sources"] if x["id"]=="psp-linux"),None)
    if source is None: raise SystemExit("PSP source record missing")
    directory=Path(sys.argv[1]) if len(sys.argv)>1 else Path("artifacts/psp-archives")
    report={"source":source["project_url"],"audit_type":"integrity-only; no extraction or execution","archives":[]}
    failures=[]
    for item in source.get("archives",[]):
        path=directory/item["id"]
        if not path.is_file(): failures.append(f"missing archive: {path}"); continue
        digest=hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda:stream.read(1024*1024),b""): digest.update(chunk)
        row={"id":item["id"],"filename":path.name,"bytes":path.stat().st_size,"sha256":digest.hexdigest(),"format":item["format"],"role":item["role"]}
        try:
            if item["format"]=="zip":
                with zipfile.ZipFile(path) as archive:
                    bad=archive.testzip()
                    if bad: raise ValueError(f"CRC failure: {bad}")
                    names=archive.namelist()
            elif item["format"]=="gzip":
                with gzip.open(path,"rb") as stream:
                    while stream.read(1024*1024): pass
                names=[]
            else: raise ValueError("unsupported format: {}".format(item["format"]))
            row["integrity"]="ok"
            row["entry_count"]=len(names)
            row["license_notice_candidates"]=[n for n in names if Path(n).name.lower() in {"license","copying","copyright","notice","licence"}]
        except (OSError,ValueError,zipfile.BadZipFile) as exc:
            row["integrity"]="failed"; row["error"]=str(exc); failures.append("{}: {}".format(item["id"], exc))
        report["archives"].append(row)
    output=directory/"psp-archive-audit.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    if failures: print("AUDIT FAILED: "+"; ".join(failures),file=sys.stderr); return 1
    if len(report["archives"])!=len(source.get("archives",[])): return 1
    print("PSP archive integrity audit: OK ({} archives; license review still required)".format(len(report["archives"])))
    return 0
if __name__=="__main__": raise SystemExit(main())
