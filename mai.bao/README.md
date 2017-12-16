# 如何创建一个名为mai.bao的包模板

## 概论：要创建 *包模板* ，在我看来，要做两件事：创建包，然后创建模板。这句话很难理解？好吧，我的意思是现在要做的是先按照创建一个包的方法来做事。

1.  第一件事：创建一个包的文件结构的命令如下：

```    
    $ mkdir -pv ./mai.bao/mai/bao
    $ cd ./mai.bao
    $ subl ./mai.bao/setup.py
    ...
```
文件结构应如下：
```
    $ find ./mai.bao
    .
    ./MANIFEST.in
    ./mai
    ./mai/__init__.py
    ./mai/bao
    ./mai/bao/__init__.py
    ./setup.py
```
- 补充：按照创建一个包的法则，./setup.py应该填写元数据代码，又在./mai/__init__.py填写命名空间声明代码。如果再规范些，比如加./README.txt，又或者加./mai/bao/docs/和./mai/bao/tests/什么的，也可以。鉴于我的目标是要总结创建 **包模板** 的方法，所以对于这些创建包的具体操作就略过了。
2.  让包变成包模板 。
2.1 修改mai.bao/setup.py:
1) 让install_requires中有 PasterScript 和 Cheetah
2) 让创建入口点entry_points:
```
    [paste.paster_create_template]
    templates_name = mai.bao.package:Package
    ...
```
2.2 创建package.py文件(亦即module)，此module即入口点指定的mai.bao.package。可以知道，这个文件提供了一个名为Package的类，此类继承自paster.script.templates.Template。
*(注：上边install_requires指定了依赖PasterScript，如果安装了，模块paster.script就可以用了)。*
2.3 提供 **模板** ，是的，划重点！ **模板** 真正地出场了，前边所做的，只是 **创建一个会生成模板的包** 而已，现在是 **包模板 = 包 + 模板** 重要时刻。
1) 我们在mai.bao/mai/bao下新建一个文件用来专门放 **模板**:
```
    $ cd mai.bao/mai/bao
    $ mkdir -pv ./tmpl/packages
```
2) 相应地，也要确认下package.py文件（不知道package.py在哪儿？）:
```
    class Package(Template):
        _template_dir = 'tmpl/packages'
        ...
```
3) 写模板，模板其实就是包（好吧...重点是，又得创建一个包):
```
    $ mkdir -pv ./ namespace/package/ && touch setup.py ...
     ...
    $ find
    .
    ./namespace
    ./namespace/__init__.py
    ./namespace/package
    ./namespace/package/__init__.py
    ./setup.py
```
4) 修改 **模板**——让上面的文件夹、文件甚至文件中的对象名 都变成变量。什么意思？还记得我们在前边有写过这样的代码吗？
```
    class Package(Template):
        _template_dir = 'tmpl/packages'
```        
我再贴下templates文件的更详细的代码吧：
```
    class Package(Template):
        _template_dir = 'tmpl/package'
        summary = "A namespaced package"
        required_templates = []
        use_cheetah = True

        vars = [
            var('namespace_package', 'Namespace package (like pbp)', 
         default='pbp'), 
            var('package', 'The package contained namespace package (like example)',
         default='example'),
            var('version', 'Version', default='0.1.0'),
            var('description', 'One-line description of the package'),
            var('long_description', 'Multi-line description (in reST)'),
            var('author', 'Author name'),
            var('author_email', 'Author email'),
            var('keywords', 'Space-separated keywords/tags'),
            var('url', 'URL of homepage'),
            var('license_name', 'License name', default='GPL'),
            var('zip_safe', 'True/False: if the package can be distributed '
      'as a .zip file', default=False),
      ] 
```
可以看到类Package定义了许多变量namespace_package package version description ... 我们修改模板，要让 **文夹名、文件名和文件中的对象名变成变量** ，就是要在上边这些变量中“随意”挑选变量名来命名文件夹名、文件名等。如，

- 用变量namespace_package 命名文件夹名./namespace,于是乎：
> ./namespace  ==>  ./+namespace_package+     ##注意要在变量名前后加+
- 用变量package 命名文件夹名./namespace/package,于是乎：
> ./namespace/package  ==>  ./+namespace_package+/+package+
- ./namespace/__init__.py也要用个变量名替换它？当然不必，因为我们知道py的包中一定要有__init__.py的，不是吗？——不过，我上文说过，要让文件中的对象名也变成变量，不是吗？难道就不看下__init__.py中的对象再作决定吗？好，我们看下__init__.py到底有什么东西。
```
    $ vim __init__.py
    try:
        __import__('pkg_resources').declare_namespace(__name__)
    except ImportError:
        from pkgutil import extend_path
        __path__ = extend_path(__path__, __name__)
```        
细数下这其中的对象：__import__,'pkg_resources', ...,完全没有类Package中的属性值嘛，所以就不用改也可以的。可是，也只是“可以的”而已。就是说如果想改的话，还是可以改改的。改哪里呢？改内容？__init__吗？当然不是，如果连这个都改了，包还是包么。要改的是.py这个后缀名，添点东西就好：
```       
    __init__.py  ==>  __init__.py_tmpl
```
5) 最后一改：修改setup.py;上面，我们想修改__init__.py没改成，原因是__init__.py中没用到（是的，没用到而已，可能会用到哦）类Package对应的属性值，而且__init__又是py包中所需要之名称。现在反观setup.py，setup当然也是python包所需要之名，所以文件名至多只能改成:
```        
    setup.py  ==>  setup.py_tmpl
```
再看setup.py中的内容：
```
    $ vim setup.py
    setup(
        name = NAME,
        version = VERSION,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ],
        keywords = KEYWORDS,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        # url = URL,
        license = LICENSE,
        packages = PACKAGES,
        include_package_data=True,
        zip_safe=True,
        install_requires=['pysqlite', 'SQLAlchemy']
    )
```
哇哇，大把Package类的属性值。所以要这样改：
> 1)Package类中有的,函数setup()也有的变量名，如：
```
version = ${repr($version)}
description = ${repr($description)}
...
```        
> 2)Package类中没有，但函数setup()中有的，却可能会在具体包中变更的：
```
    name = ${repr($project)}  ## 这个固定就如此
```        
> 3）Package类中没有，但函数setup()中有，也不会在具体包中改变的：
```
    include_package_data = True
    test_suite = 'nose.collector'
    ...             ## 这种直接不用修改，保持原样就好了
```
- 补充：上面关于package.py和setup.py_tmpl变量对应是最容易出现差错的，本人目前出现的有：
```
    1）setup.py_tmpl中
    author = ${repr($author) or $empty}, 写错成  author = ${repr(author) or $empty},
    repr后的$author 少了一个$；

    2)package.py中没有 var('author_email', 'Author email'), 却在setup.py_tmpl中有 author_email = ${repr($author_email) or $empty},
    当然这个错误应该会很少见，毕竟我是懒直接拷贝代码导致的错误；
```
3. 做完上面所有的操作，现在文件结构如下：
```
    $find ./mai.bao
    ./mai.bao/
    ./mai.bao/mai
    ./mai.bao/mai/__init__.py
    ./mai.bao/mai/bao
    ./mai.bao/mai/bao/__init__.py
    ./mai.bao/mai/bao/package.py
    ./mai.bao/mai/bao/tmpl
    ./mai.bao/mai/bao/tmpl/package
    ./mai.bao/mai/bao/tmpl/package/setup.py_tmpl
    ./mai.bao/mai/bao/tmpl/package/+namespace_package+
    ./mai.bao/mai/bao/tmpl/package/+namespace_package+/__init__.py
    ./mai.bao/mai/bao/tmpl/package/+namespace_package+/+package+
    ./mai.bao/mai/bao/tmpl/package/+namespace_package+/+package+/__init__.py
    ./mai.bao/README.txt
    ./mai.bao/setup.py
```
4. 用起来:
包模板创建完后，用起来也很简单，步骤如下：
```
    1) 首先进入./mai.bao目录下，确认setup.py在其中
    2) 使用命令：python setup.py develop 安装包模板
    3) 查看包模板是否安装成功：paster create --list-templates
    4) 使用模板：paster create -t templates_name diy_name       ##入口点：templates_name = mai.bao.package:Package
```
