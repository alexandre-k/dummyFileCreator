#!/bin/bash

##########################################################
banner(){
    echo
    echo -e "\x1B[1;33m
    \   /    ----    |
     \ /    /    \   |
      |     \    /   |
      |      ----    .

    ファイルをコピーすこととデータを増やすためのスクリプト

    By Alexandre Krispin\x1B[0m"

    echo
    echo
}

##########################################################
error(){
    echo
    echo -e "\x1B[1;31m$medium\x1B[0m"
    echo
    echo -e "\x1B[1;31m           *** 不適切や不正確な引数を入力しました。 ***\x1B[0m"
    echo -e "\x1B[1;31m          理由：" $MSG "\x1B[0m"
    echo
    echo -e "\x1B[1;31m$medium\x1B[0m"
    usage
    exit
}


##########################################################
check_original_file_existence(){
    echo
    echo -n "元のファイルの有無を確認します。"

    # Check for no parameter
    if [[ -z $1 ]]; then
        MSG="引数がありません。"
        error $MSG
    fi

    # Check for wrong parameter
    if [ ! -f $1 ]; then
        MSG="ファイルを見つかりません。"
        error
    fi
}

##########################################################
check_destination_file_existence(){
    echo
    echo -n "宛先ファイルの有無を確認します。"

    # Check for no parameter
    if [[ -z $1 ]]; then
        error
    fi

    # Check for already existing file
    if [ -f $1 ]; then
        MSG='ファイルは既に存在します。'
        error $MSG
    fi
}

##########################################################
check_required_size() {
    echo
    echo -n "ファイルサイズを確認します。"

    # Check for no parameter
    if [[ -z $1 ]]; then
        error
    fi

    # Check size type
    [[ $1 =~ ([0-9]+) ]] && CLEANED_SIZE="${BASH_REMATCH[1]}"

    if [[ $1 =~ .*KB ]]; then
        SIZE=$(($CLEANED_SIZE * 1000))
    fi

    if [[ $1 =~ .*MB ]]; then
        SIZE=$(($CLEANED_SIZE * 1000000))
    fi

    if [[ $1 =~ .*GB ]]; then
        SIZE=$(($CLEANED_SIZE * 1000000000))
    fi
}

##########################################################
arg_handler() {
    if [[ -z $1 ]]; then
        usage
    fi

    while [[ $1 ]]
    do
        case "$1" in
            -f)
                check_original_file_existence $2
                ORIGINAL_FILE="$2"
                ACTUAL_SIZE=$(stat --format=%B --printf='%s' $ORIGINAL_FILE)
                shift 2
                ;;
            -d)
                check_destination_file_existence $2
                DESTINATION_FILE="$2"
                shift 2
                ;;
            -s)
                check_required_size $2
                REQUIRED_SIZE=$SIZE
                shift 2
                ;;
            *)
                usage
                ;;
        esac
    done
}

##########################################################
terminate() {
    echo "完了しました。"
    echo "新規のファイルを保存しました。"
    exit
}

##########################################################
usage() {
    echo -e '使用方法：\e[33mbash \e[35m'$(basename $0)' \e[32m-f 元のファイル名  \e[34m-d 宛先ファイル名  \e[36m-s サイズ'
    echo -e '\e[39m-------------------------------------'
    echo -e '\e[39m引数の説明：'
    echo -e '\e[39m-------------------------------------'
    echo -e '\e[32mf: 既存のファイルを入力します。スクリプトのディレクトリに位置しているファイルです。'
    echo -e '\e[34md: 新規のファイルを作成しますから、同じディレクトリに既にファイルが在ればエラーが出てしまいます。'
    echo -e '\e[36ms: 数字プラスKBやMBやGBを指定します。例：123KB、13MB、1GB。'
    echo -e '\e[39m-------------------------------------'
    echo -e '\e[37m実行例：'$(basename $0) '-f myfile.csv -d dest_file.csv -s 5MB'
    exit
}

##########################################################
check_variables() {
    echo 'ORIGINAL FILE: ' $ORIGINAL_FILE
    echo 'DESTINATION FILE: ' $DESTINATION_FILE
    echo 'ACTUAL SIZE IN BYTES: ' $ACTUAL_SIZE
    echo 'REQUIRED SIZE IN BYTES: ' $REQUIRED_SIZE
}

##########################################################
display_size() {

    SIZE_IN_KB=$(( $ACTUAL_SIZE / 1024 ))
    SIZE_IN_MB=$(( $SIZE_IN_KB / 1024 ))
    # SIZE_IN_GB=$((SIZE_IN_MB/1024))

    if [[ $ACTUAL_SIZE -le 1000 ]]; then
        echo -ne '\t宛先ファイルのサイズは' $ACTUAL_SIZE 'Bytes'
    fi

    if [[ $ACTUAL_SIZE -ge 1000 ]] && [[ $ACTUAL_SIZE -le 1000000 ]]; then
        echo -ne '\t宛先ファイルのサイズは' $SIZE_IN_KB 'KB ('$ACTUAL_SIZE Bytes')'
    fi

    if [[ $ACTUAL_SIZE -ge 1000000 ]]; then
        echo -ne '\t宛先ファイルのサイズは' $SIZE_IN_MB 'MB (' $SIZE_IN_KB KB')'
    fi

    # if [[ $ACTUAL_SIZE -ge 1000000000 ]]; then
        # echo -ne '宛先ファイルのサイズは' $SIZE_IN_GB 'GB'
    # fi
}

##########################################################
copy_file() {
    # Loop until the required size of thedestination file
    # becomes greater than its actual size
    echo -e ${ORIGINAL_FILE}' から'${DESTINATION_FILE}' へコピー中。。。'
    echo '中止するためにCtrl+Cキーを押下してください。'

    spin='-\|/'
    i=0

    while [[ "$ACTUAL_SIZE" -le "$REQUIRED_SIZE" ]]
    do
        # Copying existing lines to new file
        cat $ORIGINAL_FILE | while read line
        do
            echo $line  >> $DESTINATION_FILE
            i=$(( (i+1) % 4 ))
            printf "\r${spin:$i:1}"
        done

        #Recompute the size of new the file after copying it completely one time
        ACTUAL_SIZE="$(stat --format=%B --printf='%s' $DESTINATION_FILE)"
        display_size $ACTUAL_SIZE
    done
}


##########################################################
main() {
    clear
    banner
    arg_handler $@
    check_variables
    copy_file  $ACTUAL_SIZE $REQUIRED_SIZE $ORIGINAL_FILE $DESTINATION_FILE
    # ORIGINAL_FILE='text.csv'
    # while read line
    # do
        # echo $line
    # done < $ORIGINAL_FILE

}

main $@

