
```bash
#!/bin/bash
#cpdir.sh
#此脚本用于复制源目录的目录，不复制源目录中的文件，确保目的目录中均为空目录。
usage()
{
    echo "cpdir.sh source_dir destination_dir"
}

if [ $# -ne 2 ]
then
{
    usage
    exit 0
}
fi

srcdir=$1
desdir=$2

if [ ! -d $srcdir ]
then
{
    usage
    echo "error: source_dir ($srcdir) is not a directory."
    exit
}
fi

if [ ! -d $desdir ]
then
{
    usage
    echo "error: destination_dir ($desdir) is not a directory."
    exit
}
fi

processid=$$;

echo "source directory($srcdir)的所有子目录"
echo "--------------------------------"
find $srcdir/* -type d | /usr/bin/tee /tmp/srcdir_tmp_${processid}.txt
sed "s/^${srcdir}/${desdir}/g" /tmp/srcdir_tmp_${processid}.txt > /tmp/srcdir_${processid}.txt

rm -rf ${desdir}/*
for subdir in `cat /tmp/srcdir_${processid}.txt`
do
{
    mkdir ${subdir}
}
done
echo "destination directory ($desdir) 所有子目录"
echo "--------------------"
find $desdir/* -type d|/usr/bin/tee /tmp/desdir_${processid}.txt

echo ""
echo "compare source directory with destination directory"
echo "------------------------"
diff /tmp/desdir_${processid}.txt /tmp/srcdir_${processid}.txt

rm -f /tmp/srcdir_${processid}.txt
rm -f /tmp/srcdir_tmp_${processid}.txt
rm -f /tmp/desdir_${processid}.txt

```


