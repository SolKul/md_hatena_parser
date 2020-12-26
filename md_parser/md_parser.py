from pathlib import Path
import os,re
import markdown as md

def classfy_math_block(md_list,pos,end_pos):
    """
    ブロック環境の数式を検知する。
    """
    # $$があるかどうか。
    if ('$$' in md_list[pos]):
        math_block_start_pos=pos
        # 終わりの$$が出てくるまで読み込む
        for i in range(pos+1,end_pos):
            if '$$' in md_list[i]:
                math_block_end_pos=i
                break
        math_block=md_list[math_block_start_pos:math_block_end_pos+1].copy()
        # ブロックの種類とブロックのリストをタプルにする
        block_tuple=("math_block",math_block)
        # タプルとブロックの終わりの位置を返す
        return block_tuple,math_block_end_pos
    else:
        # $$が無い場合
        return None,pos

# ブロック環境の数式の始まりと終わり
block_begin="<div align=\"center\">[tex:\displaystyle{ "
block_end=" }]</div>"
# ブラケットの正規表現
bracket_begin_pat=re.compile(r'\[')
bracket_end_pat=re.compile(r'\]')
# 不等号の正規表現
less_than_pat=re.compile(r'<')
more_than_pat=re.compile(r'>')

def parse_math_block(math_block):
    """
    ブロック環境の数式をパースすする。
    """
    new_math_list=[block_begin]
    for i in range(1,len(math_block)-1):
        line=math_block[i].rstrip(os.linesep)
        line=bracket_begin_pat.sub('\\[', line)
        line=bracket_end_pat.sub('\\]', line)
        line=less_than_pat.sub(' < ',line)
        line=more_than_pat.sub(' > ',line)
        line=re.sub(r'aligned',r'align',line)
        new_math_list.append(line)
    new_math_list.append(block_end)
    return "".join(new_math_list)

# インライン環境の数式の正規表現
inline_dollar_pat=re.compile(r'\$(.+?)\$')
# インライン環境の数式の始まりと終わり
# \が4つなのは、もともと必要な\のエスケープに加え、
# re.sub()のreple引数で使うので、
# reple引数では\を解釈してしまうのでそれをエスケープするため。
inline_begin="[tex:\\\\displaystyle{"
inline_end="}]"

# h2タグの始まりと終わり
h3tag_begin_pat=re.compile(r"<h3>")
h3tag_end_pat=re.compile(r"</h3>")
# h3タグの始まりと終わり
h4tag_begin=r"<h4>"
h4tag_end=r"</h4>"

# h2タグの始まりと終わり
h2tag_begin_pat=re.compile(r"<h2>")
h2tag_end_pat=re.compile(r"</h2>")
# h3タグの始まりと終わり
h3tag_begin=r"<h3>"
h3tag_end=r"</h3>"


def parse_plain_block(plain_block):
    """
    mdモジュールで変換した後、
    インライン環境の数式をパースし、
    h3タグをh4に、h2タグをh3にする。
    """
    md_parser=md.Markdown(extensions=['tables'])

    parsed=md_parser.convert("".join(plain_block))
    parsed=inline_dollar_pat.sub(inline_begin+r"\1"+inline_end,parsed)
    
    parsed=h3tag_begin_pat.sub(h4tag_begin,parsed)
    parsed=h3tag_end_pat.sub(h4tag_end,parsed)
    
    parsed=h2tag_begin_pat.sub(h3tag_begin,parsed)
    parsed=h2tag_end_pat.sub(h3tag_end,parsed)
    return parsed

def classify_blocks(md_whole):
    """
    文章全体を標準ブロック、数式ブロックなどとブロックごとのリストに分ける
    """
    # 今何行目か(position)
    pos=0
    previous_pos=0
    # ブロックのリスト
    md_block_list=[]
    end_pos=len(md_whole)
    for i in range(end_pos):
        # 行数が最終行以降であれば、抜ける
        if pos >= end_pos:
            plain_block=md_whole[previous_pos:pos].copy()
            md_block_list.append(
                ("plain_block",
                plain_block)
            )
            break
        block_tuple,block_end_pos=classfy_math_block(md_whole,pos,end_pos)
        # ブロックが検知された場合は
        if block_tuple is not None:
            # 標準ブロックをplain_blockとしてタプルにし追加
            plain_block=md_whole[previous_pos:pos].copy()
            md_block_list.append(
                ("plain_block",
                plain_block)
            )
            # 今回検知されたブロックを追加
            md_block_list.append(block_tuple)
            # 行数をブロックの最終行に
            pos=block_end_pos
            previous_pos=block_end_pos+1
        pos+=1
    return md_block_list

def parse_block_list(md_block_list):
    """
    ブロックのリストそれぞれをパースする
    """
    parsed_list=[]

    for block in md_block_list:
        if block[0] == "plain_block":
            parsed_list.append( parse_plain_block(block[1]) )
        elif block[0] == "math_block":
            parsed_list.append( parse_math_block(block[1]))
    return parsed_list

        
def parse_md_to_hatena(md_path):
    """
    pathlibのPathを受け取って、
    markdownをはてな記法にパースして、
    もとのファイル名_hatena.txtとして保存する
    """
    with md_path.open(encoding='utf-8',mode='r') as f:
        md_whole=f.readlines()

    if md_whole is None:
        return None
    md_block_list=classify_blocks(md_whole)
    parsed_list=parse_block_list(md_block_list)

    # 保存する
    hatena_path=Path(md_path.stem+"_hatena.txt")
    hatena_path.write_text("\n".join(parsed_list),encoding='utf-8')