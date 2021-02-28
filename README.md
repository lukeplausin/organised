# Organized

* Are you hopelessly disorganized?
* Do you have lots of folders on your desktop named "stuff", "todo", "sort me" etc?
* Are there many sets of old pictures and photographs scattered around your hard disk and various cloud providers which you want to consolidate?

If you answered yes to any of the above, then this project might be able to help you.

# Features

What the project can do for you already:
* Arrange photos based on exif tags
* Clean up junk files

What I want the project to do soon:
* Archive old git repositories
* Find files which are problematic or cause issues
* Recommend files for compression or deletion
* Identify duplicate photos or files
* Produce some nice easy to view visualisations of your mess to help you decide what to do with it
* Run continuously to sort through and arrange files which you dumped on the desktop or into a 'sort-me' folder
* Suggestions welcome!

# Install

```bash
pip install git+https://github.com/lukeplausin/organised.git
```

The tool has a comprehensive CLI based on python click. It is self documenting, so you can use the `--help` parameter on any command or subcommand to check the helptext.

```
# Show help text
organize photos --help
```

# Usage

## Photo sorter

This is a command line tool which can arrange your photos based on EXIF tags. You as the end user can specify where to move files from and to, and what format to save them in at the destination.

This is useful for people who may have a lot of photos taken over the years with different devices and various naming conventions.

Example:

```
(Before)
[jumbled mess of photos in random folders with no recognisable pattern of filenames or structure]

(After)
~/Pictures/Camera
├── 2016-08 (SM-G900F)
│   ├── 20160812_170344.jpg
│   └── 20160812_170409.jpg
├── 2016-10 (SM-G900F)
│   ├── 20161007_220124.jpg
│   ├── 20161007_220247.jpg
│   ├── 20161007_223224.jpg
│   ├── 20161007_223539.jpg
│   ├── 20161008_021820.jpg
├── 2019-03 (Nokia 5.1)
│   ├── 20190301_143505.jpg
│   ├── 20190301_144631.jpg
│   ├── 20190302_161408.jpg
...
```

```
# Run photo organiser with default options
organize photos ~/camera/old_stuff

# Run photo organiser in dry-run mode (doesn't do anything it just says what it is going to do)
organize photos ~/camera/old_stuff --dry-run

# Run organiser with custom options - data from exif is specified in curly braces {}
organize photos ~/camera/old_stuff --base-path ~/Pictures/Camera --file-path "{Date:%Y-%m-%d_%H:%M:%S}.{File_FileTypeExtension}"

# Run with prompt (asks you before doing anything)
organize photos ~/camera/old_stuff --prompt
```

## A word on spelling

Although in my country organise is spelled with an "s", spelling conventions in code tend to take after the U, so for this reason I have decided to use "organize" with a Z throughout the source code. When you install the python module, the CLI scripts are installed to the system with both british and american spellings so this should keep everyone happy.

```bash
organise --help
organize --help
org --help
```
