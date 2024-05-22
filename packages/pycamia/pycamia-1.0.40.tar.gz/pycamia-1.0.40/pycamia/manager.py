
__info__ = dict(
    project = "PyCAMIA",
    package = "<main>",
    author = "Yuncheng Zhou",
    create = "2021-12",
    fileinfo = "File to manage package info.",
    help = "Use `info_manager(**kwargs)` to create an info object and use `with info` to check for imports. "
)

__all__ = """
    info_manager
    Hyper
    hypers
    Version
    Args
    args
""".split()

import os, re, sys, time, builtins, types
from optparse import OptionParser
from argparse import ArgumentParser

from .environment import get_environ_vars
from .strop import tokenize

update_format = "%Y-%m-%d %H:%M:%S"

class Version(tuple):
    def __new__(cls, string):
        matches = re.findall(r"[0-9\.]+", string)
        if len(matches) == 0: raise TypeError(f"{string} is not a version")
        return super().__new__(cls, [eval(x) for x in matches[0].split('.') if x])
    for op in "gt lt ge le eq ne".split():
        exec(f"def __{op}__(self, x): return super(Version, self).__{op}__(Version(x) if isinstance(x, str) else x)")

class info_manager:
    """
    info_manager() -> info_object

    An object storing the info of the current file.

    Note:
        It is currently provided for private use in project PyCAMIA only. 
        But it can also be used outside.

    Examples::
        Code.py:
            __info__ = info_manager(
                project="PyCAMIA", 
                package="", 
                requires="xxx"
            ).check()
            print("Project is", __info__.project)
            with __info__:
                import xxx
                from xxx import yyy
        Output:
            Project is PyCAMIA
        Error if xxx doesnot exist: ModuleNotFoundError
        Error if yyy doesnot exist in xxx: ImportError
    """
    
    @staticmethod
    def parse(code):
        info = eval(code)
        raw_args = tokenize(code, sep=['(',')'])[1]
        info.tab = raw_args[:re.search(r'\w', raw_args).span()[0]].strip('\n')
        info.order = tokenize(raw_args, sep=[',', '='], strip=None)[::2]
        return info

    def __init__(self, project = "", package = "", requires = "", **properties):
        if isinstance(requires, str): requires = requires.split()
        properties.update(dict(project=project, package=package, requires=requires))
        self.properties = properties
        self.__dict__.update(properties)
        env = get_environ_vars()
        file_path = env['__file__']
        file = os.path.extsep.join(os.path.basename(file_path).split(os.path.extsep)[:-1])
        self.name = '.'.join([x for x in [project, package, file] if x and x != "__init__"])
        self.tab = ' ' * 4
        major_keys = "project package requires".split()
        self.order = major_keys + list(set(properties.keys()) - set(major_keys))
        env['__args__'] = Args(sys.argv)
        
    def check_requires(self):
        not_found_packages = []
        for r in self.requires:
            tokens = tokenize(r, ['<', '>', '='], strip=None, keep_empty=False)
            if len(tokens) == 2: rname, rversion = tokens
            else: rname, rversion = tokens[0], None
            try:
                package = __import__(rname)
            except ModuleNotFoundError: not_found_packages.append(rname)
            if rversion is not None:
                op = r.replace(rname, '').replace(rversion, '').strip()
                if not eval("Version(package.__version__)" + op + "'" + rversion + "'"):
                    not_found_packages.append(r)
        if len(not_found_packages) > 0:
            raise ModuleNotFoundError(f"'{self.name}' cannot be used without dependencies {repr(not_found_packages)}.")
            
    def check(self):
        self.check_requires()
        return self
    
    def version_update(self):
        if hasattr(self, 'version'):
            version = re.sub(r"((\d+\.){2})(\d+)", lambda x: x.group(1)+str(eval(x.group(3))+1), self.version)
        else: version = '1.0.0'
        self.version = version
        self.update = time.strftime(update_format, time.localtime(time.time()))
    
    def __enter__(self): return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == ModuleNotFoundError:
            module_name = str(exc_value).split("'")[-2]
            raise ModuleNotFoundError(f"'{self.name}' cannot be used without dependency '{module_name}'. ")
        elif exc_type == ImportError:
            module_name, _, func_name = str(exc_value).split("'")[1:4]
            raise ImportError(f"'{self.name}' requires '{func_name}' in module '{module_name}'. Please double check the version of packages. ")
        
    def __str__(self):
        args = ',\n'.join([self.tab + k + ' = ' + repr(getattr(self, k)) for k in self.order])
        return "info_manager(\n" + args + "\n)"
    
    def __getitem__(self, name):
        return getattr(self, name)
    
    def __setattr__(self, name, value):
        if hasattr(self, 'order') and name not in self.order: self.order.append(name)
        super().__setattr__(name, value)
    
    def get(self, name, value):
        if hasattr(self, name): return self[name]
        return value

class Hyper:
    def __init__(self):
        self.optParser = OptionParser()

    def add_hyper(self, *names, default=None, type=None, help_str='', **kwargs):
        if 'name' in kwargs: names += (kwargs['name'],)
        if len(names) == 0: raise TypeError("add_hyper requires a name. ")
        if type is None: type = builtins.type(default)
        if help_str == '': help_str = f"variable \'{kwargs.get('name', names[0])}\'"

        new_names = []
        for name in names:
            name = name.lstrip('-')
            abbr_match = re.match(r'\[(.)\]', name)
            if abbr_match is not None:
                abbr = abbr_match.group(1)
                name = name[:abbr_match.span()[0]] + abbr + name[abbr_match.span()[1]+1:]
                new_names.extend([f'-{abbr}', f'--{name}'])
            else:
                new_names.append(('-' if len(name) > 1 else '') + f'-{name}')

        if type == bool:
            self.optParser.add_option(
                *new_names, action = 'store_true' if default else 'store_false', 
                dest = name, default = default, help = help_str
            )
        else:
            self.optParser.add_option(
                *new_names, action = 'store', type = type, 
                dest = name, default = default, help = help_str
            )
            
    def parse_args(self, *args):
        res = self.optParser.parse_args(*args)
        self.__dict__.update(vars(res[0]))
        return res
    
    def parse_name(self, *args):
        self.parse_args(*args)
        return str(self)

    def __str__(self):
        defaults = vars(self.optParser.get_default_values())
        values = vars(self)
        values.pop('optParser')
        updated = {k: v for k, v in values.items() if k in defaults and v != defaults[k]}
        if len(updated) == 0: return "baseline"
        token = lambda k, v: str(k) + '_' + re.sub(r'\.0+$', '', str(v)[-10:])
        return '-'.join([token(k, v) for k, v in updated])

def hypers(**kwargs):
    hyper = Hyper()
    for k, v in kwargs.items():
        hyper.add_hyper(k, default=v, help_str=kwargs.get(k+'_help', ''))
    variables, args = hyper.parse_args(sys.argv)
    vs = get_environ_vars()
    vs.update(vars(variables))
    return hyper

class const:

    value = None
    
    @classmethod
    def __class_getitem__(cls, value):
        cls.value = value
        return cls

class Args:
    
    """
    Argument manager for a python script. An enclosure of argparse.ArgumentParser. 

    Example::
        >>> args = Args("a.py -fv --n_epoch 4 --n_batch 3".split()[1:])
        >>> args.n_epoch = 5
        >>> args.n_batch[int: "The batch size for the network training. "] = 5
        >>> args.gpu[list[2]: "The 2 GPU ids. "] = [2, 3]
        >>> with args('-f'): args.flag[bool: "A flag argument which is False if --flag is not given. "] = False
        >>> with args('-v', '--use_valid'): args.n_iter_each_valid[Args.const[10]: "Whether to use validation or not. "] = int(1e6)
        >>> args
        Args(n_epoch=4, n_batch=3, gpu=[2, 3], flag=True, n_iter_each_valid=10)
        >>> args.n_batch
        3
        >>> print(args.help())
        usage: <code> [-h] [--n_epoch N_EPOCH] [--n_batch N_BATCH] [--gpu GPU GPU] [-f [FLAG]] [-v [N_ITER_EACH_VALID]]

        options:
        -h, --help            show this help message and exit
        --n_epoch N_EPOCH     The maximal number of epochs for training.
        --n_batch N_BATCH     The batch size for the network training.
        --gpu GPU GPU         The 2 GPU ids.
        -f [FLAG]             A flag argument which is False if --flag is not given.
        -v [N_ITER_EACH_VALID], --use_valid [N_ITER_EACH_VALID]
                                Whether to use validation or not.
    """
    
    default_help_strs = dict(
        n_batch = "Batch size for each iteration. ", 
        batch_size = "Batch size for each iteration. ", 
        n_epoch = "The maximal number of epochs for training. ", 
        epochs = "The maximal number of epochs for training. ", 
        max_epoch = "The maximal number of epochs for training. ", 
        init_epoch = "The index of epoch for the first iteration, used in restarts of training. ",
        i_gpu = "The id of GPU(s)", 
        gpu = "The id of GPU(s)", 
    )
    
    const = const
    
    @staticmethod
    def tags(self, name):
        abbr_match = re.match(r'\[(.)\]', name)
        if abbr_match is not None:
            abbr = abbr_match.group(1)
            name = name[:abbr_match.span()[0]] + abbr + name[abbr_match.span()[1]+1:]
            names=[f'-{abbr}', f'--{name.lstrip("-")}']
        else:
            names=[('-' if len(name) > 1 else '') + f'-{name}']
        return names
    
    class Arg:
        def __init__(self, parent, name):
            self.parent = parent
            self.name = name
            
        def __setitem__(self, subscript, value):
            if isinstance(subscript, str):
                _type = value.__class__
                _help = subscript
            elif isinstance(subscript, type):
                _type = subscript
                _help = Args.default_help_strs.get(self.name, f"Argument '{self.name}' for {self.parent.parser.prog}. ")
            elif isinstance(subscript, slice):
                if subscript.step is not None: raise TypeError("Only one colon is allowed in argument expression. ")
                _type = subscript.start
                _help = subscript.stop
            if _type == Args.const: nargs = '?'; const = _type.value; _type = type(_type.value)
            elif _type == bool: nargs = '?'; const = True
            else:
                if not isinstance(_type, (type, types.GenericAlias)): raise TypeError("Only types or Args.const is allowed before colon. ")
                if issubclass(_type, (tuple, list)) and isinstance(_type, types.GenericAlias):
                    nargs = _type.__args__[0]
                    nargs = {'>0': '+', slice(None): '+', ...: '*', -1: '*'}.get(nargs, nargs)
                nargs = (len(value) if len(value) > 0 else '*') if isinstance(value, (tuple, list)) else None
                const = None
            tags = self.parent.additional_tags
            if not tags: tags = ['--' + self.name]
            if '--' + self.name not in tags: dest = self.name
            else: dest = None
            self.parent.parser.add_argument(*tags, action='store', nargs=nargs, const=const, dest=dest, type=_type, default=value, help=_help)
            self.parent.valid_tags.extend(tags)
            self.parent.arg_names.append(self.name)
            if not self.parent.parse_attempt():
                setattr(self.parent, self.name, value)
            
    class Scope:
        
        def __init__(self, parent, *tags):
            if len(tags) == 1 and isinstance(tags[0], (tuple, list)): tags = tags[0]
            self.tags = list(tags)
            self.parent = parent
            
        def __enter__(self): self.parent.additional_tags = self.tags
        def __exit__(self, type, value, trace): self.parent.additional_tags = []

    properties = ['argv', 'parser', 'arg_names', 'valid_tags', 'additional_tags']
    
    def __init__(self, argv=None, **kwargs):
        if argv is None: prog, *argv = sys.argv
        else: prog = '<code>'
        self.argv = argv
        self.parser = ArgumentParser(prog=prog, **kwargs)
        self.arg_names = []
        self.valid_tags = ['-h', '--help']
        self.additional_tags = []
    
    def __getattribute__(self, name):
        try: return super().__getattribute__(name)
        except AttributeError:
            return Args.Arg(self, name)
    
    def __setattr__(self, name, value):
        if name in Args.properties: return super(Args, self).__setattr__(name, value)
        if name in self.arg_names: return super(Args, self).__setattr__(name, value)
        help_str = Args.default_help_strs.get(name, f"Argument '{name}' for {self.parser.prog}. ")
        tags = self.additional_tags
        if not tags: tags = ['--' + name]
        if '--' + name not in tags: dest = name
        else: dest = None
        self.parser.add_argument(*tags, action='store', dest=dest, type=type(value), default=value, help=help_str)
        self.valid_tags.extend(tags)
        self.arg_names.append(name)
        if not self.parse_attempt():
            return super(Args, self).__setattr__(name, value)
        
    def __call__(self, *tags):
        return Args.Scope(self, *tags)
    
    def parse_attempt(self, input_argv=None):
        if input_argv is None: input_argv = self.argv
        argv = []
        for va in input_argv:
            if not va.startswith('-'): argv.append(va); continue
            if va in self.valid_tags: argv.append(va); continue
            for t in va[1:]:
                if t == '-': break
                if '-'+t not in self.valid_tags: break
            else: argv.extend(['-'+t for t in va[1:]]); continue
            return False
        args = self.parser.parse_args(argv)
        for k, v in args._get_kwargs(): setattr(self, k, v)
        return True
    
    def help(self):
        return self.parser.format_help()
    
    def __str__(self):
        return f"Args({', '.join(f'{a}={getattr(self, a)}' for a in self.arg_names)})"
    
    __repr__ = __str__
    
args = Args()
