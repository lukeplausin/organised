# Organized

* Are you hopelessly disorganized?
* Do you have lots of folders on your desktop named "stuff", "todo", "sort me" etc?
* Are you always having trouble finding your files?
* Are there many sets of old photos scattered around your hard disk and various cloud providers which you want to consolidate?

If you answered yes to any of the above, then this project might be able to help you.

# Philosophy

`A place for everything and everything in it's place`

This is the key to being well organized.

If you are well organised, then you will be more productive and are more likely to achieve your goals and be successful. This is what we get taught growing up and in school - but there are many of us who are well organised at work but have messy lives at home or in the virtual world. It's understandable.. who would want to spend their precious time after work sorting through virtual photo albums or the gigabytes of stuff which you accumulated over the last few years.

The aim of this project is to help you become better organised in your digital life while saving time and doing the boring bits for you. You just tell the project where and how you want your files saved, and the code does the rest for you!

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

## Junk finder

This utility allows you to find and track down files which might be unwanted. As an example, I use it to delete empty folders, and remove the `.DS_Store` files which my Mac leaves everywhere.

You can customise the file names or extensions which you regard as junk and can switch the empty folder deletion on or off with a command line parameter. The de-junker works recursively through a folder structure so it's useful if you want to repeat an operation throughout a file tree.

```
organize dejunk --dry-run --prompt --no-cleanup-empty-dirs --junk-filenames ".DS_Store" --junk-filenames ".db"
```

# A word on spelling

In my country 🇬🇧 organise is spelled with an "s", however international code conventions tend to use US spelling so for this reason I've decided to use "organize" (with a Z) throughout the source code. When you install the python module, the CLI scripts are installed to the system with both British and American spellings so this should keep everyone happy.

```bash
organise --help
organize --help
org --help
```
