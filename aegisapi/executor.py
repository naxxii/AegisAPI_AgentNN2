import subprocess, pathlib
from .telemetry import log_event
def _run(cmd, out):
    res = subprocess.run(cmd, capture_output=True, text=True)
    pathlib.Path('reports').mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(res.stdout + '\n---\n' + res.stderr, encoding='utf-8')
    return res.returncode
def run_tests(tests_dir, spec, base_url, with_fuzz=False):
    code_py=_run(['pytest','-q',tests_dir,'--junitxml','reports/junit.xml'],'reports/pytest_stdout.txt')
    log_event({'type':'run_summary','summary':f'pytest_return={code_py}'})
    code_st=0
    if with_fuzz:
        code_st=_run(['schemathesis','run',spec,'--checks','all','--base-url',base_url,'-q'],'reports/schemathesis.txt')
        log_event({'type':'fuzz_summary','summary':f'schemathesis_return={code_st}'})
    return 0 if code_py==0 and code_st==0 else 1
