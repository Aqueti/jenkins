f_name=$1
SIZE=24

if [[ -z "$f_name" ]]; then
  echo "no file specified"
  exit 1;
elif [[ ! -f ${f_name} ]]; then
  echo "file not found"
  exit 1;
elif [[ ${f_name: -3} != ".gz" ]]; then
  echo "not gzip archive"
  exit 1;
fi

f_size=`du -m ${f_name} | cut -f1`
if (( f_size < ${SIZE} )); then
  echo "file size is <${SIZE}mb"
  exit 0;
fi

gunzip $f_name
nef_name=$(echo "$f_name" | cut -f 1 -d '.')

p=$(( (${f_size} + 0)/${SIZE} + 1 ))
pp=$(( (`wc -l < ${nef_name}` + 1)/${p} ))

split -l${pp} --numeric-suffixes ${nef_name} ${nef_name}_part

for file in ${nef_name}_part*; do
  gzip ${file}
  echo ${file}.gz
done

gzip ${nef_name}
