
import importlib.util, sys, types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SessionState(dict):
    def __getattr__(self, key):
        try: return self[key]
        except KeyError: raise AttributeError(key)
    def __setattr__(self, key, val): self[key] = val

class Dummy:
    def __enter__(self): return fake
    def __exit__(self, *args): return False
    def __getattr__(self, name): return getattr(fake, name)

class Sidebar:
    def markdown(self,*a,**k): pass
    def caption(self,*a,**k): pass
    def radio(self, label, options, index=0, **k): return options[index]
    def text_input(self, label, key=None, value="", **k):
        if key:
            fake.session_state[key]=fake.session_state.get(key, value)
            return fake.session_state[key]
        return value
    def selectbox(self, label, options, index=0, **k): return options[index]
    def file_uploader(self,*a,**k): return None
    def success(self,*a,**k): pass
    def error(self,*a,**k): pass
    def warning(self,*a,**k): pass
    def info(self,*a,**k): pass
    def download_button(self,*a,**k): return False
    def button(self,*a,**k): return False

class Fake(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state=SessionState()
        self.sidebar=Sidebar()
    def set_page_config(self,*a,**k): pass
    def markdown(self,*a,**k): pass
    def write(self,*a,**k): pass
    def caption(self,*a,**k): pass
    def subheader(self,*a,**k): pass
    def metric(self,*a,**k): pass
    def dataframe(self,*a,**k): pass
    def plotly_chart(self,*a,**k): pass
    def info(self,*a,**k): pass
    def warning(self,*a,**k): pass
    def success(self,*a,**k): pass
    def error(self,*a,**k): pass
    def text_input(self, label, value="", key=None, **k):
        if key:
            self.session_state[key]=self.session_state.get(key, value)
            return self.session_state[key]
        return value
    def text_area(self,*a,**k): return ""
    def file_uploader(self,*a,**k): return None
    def download_button(self,*a,**k): return False
    def button(self,*a,**k): return False
    def slider(self, label, min_value=None, max_value=None, value=None, step=None, **k): return value
    def selectbox(self, label, options, index=0, **k): return options[index]
    def radio(self, label, options, index=0, **k): return options[index]
    def columns(self, spec, **k):
        n=spec if isinstance(spec,int) else len(spec)
        return [Dummy() for _ in range(n)]
    def expander(self,*a,**k): return Dummy()
    def rerun(self): pass

def main():
    global fake
    fake=Fake()
    sys.modules["streamlit"]=fake
    spec=importlib.util.spec_from_file_location("app", ROOT/"app.py")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for page in ["dashboard","data","signal","workflow","twin","oee","requirements","about"]:
        fake.session_state.page=page
        mod.main()
        print("OK", page)
    print("APP MOCK TESTS PASSED")

if __name__=="__main__":
    main()
