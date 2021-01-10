from pathlib import Path
import os,re
import markdown as md
import urllib.request

# mathjax-nodeを使って
# 数式をSVGに変換するnodeのURL
url = 'http://localhost:8080/convert'
headers = {
    'Content-Type': 'text/plain',
}

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
# パース後のブラケット
parsed_bracket_begin=r'\['
parsed_bracket_end=r'\]'

# svgの場合のブロック数式の始まりと終わり
div_begin="<div align=\"center\">"
div_end="</div>"
 
# 不等号の正規表現
less_than_pat=re.compile(r'<')
greater_than_pat=re.compile(r'>')
# パース後の不等号
# \\が2つなのに更にraw文字列としているのは、
# もともと必要な\のエスケープに加え、
# re.sub()のreple引数で使うので、
# reple引数では\を解釈してしまうのでさらにそれをエスケープするため。
parsed_less_than=r'\\lt '
parsed_greater_than=r'\\gt '

def parse_math_block(math_block,svg=False):
    """
    ブロック環境の数式をパースする。
    """
    if svg:
        whole_mb="".join(math_block[1:-1])
        req = urllib.request.Request(url,whole_mb.encode(),headers)
        with urllib.request.urlopen(req) as res:
            body=res.read().decode("utf-8")
            parsed_math_block = \
                div_begin + body + div_end
             
    else:
        new_math_list=[block_begin]
        for i in range(1,len(math_block)-1):
            line=math_block[i].rstrip(os.linesep)
            # ブラケットをエスケープする
            line=bracket_begin_pat.sub(parsed_bracket_begin, line)
            line=bracket_end_pat.sub(parsed_bracket_end, line)
            # 不等号をMathJax用不等号記号に
            line=less_than_pat.sub(parsed_less_than,line)
            line=greater_than_pat.sub(parsed_greater_than,line)
            line=re.sub(r'aligned',r'align',line)
            new_math_list.append(line)
        new_math_list.append(block_end)
        parsed_math_block="".join(new_math_list)
    return parsed_math_block

# インライン環境の数式の正規表現
inline_dollar_pat=re.compile(r'\$(.+?)\$')
# ブラケットの正規表現
bracket_begin_pat=re.compile(r'\[')
bracket_end_pat=re.compile(r'\]')
# 不等号の正規表現
less_than_pat=re.compile(r'<')
greater_than_pat=re.compile(r'>')
# インライン環境の数式の始まりと終わり
inline_begin=r"[tex:\displaystyle{ "
inline_end=" }]"
 
class InlineMath:
    """
    標準ブロック中の一つ一つのインライン数式のクラス
    元の数式と、標準ブロック中何番目のインライン数式かを引数にとる。
    """
    math_prefix="inline_math_"
    
    def __init__(
            self,
            inline_math_str,
            match_no,
            svg=False):
        self.inline_math_str=inline_math_str
        self.match_no=match_no
        
        #「inline_math_数字」という文字列を作成する
        self.rpl_str="{}{:0=4}".format(
            type(self).math_prefix,
            match_no)

        conv_math_str=inline_math_str
        if svg:
            req = urllib.request.Request(
                url,
                conv_math_str.encode(),
                headers)
            with urllib.request.urlopen(req) as res:
                conv_math_str=res.read().decode("utf-8")
        else:
            # ブラケットをエスケープする
            conv_math_str=bracket_begin_pat.sub(parsed_bracket_begin, conv_math_str)
            conv_math_str=bracket_end_pat.sub(parsed_bracket_end, conv_math_str)
            # 不等号をMathJax用不等号記号に
            conv_math_str=less_than_pat.sub(parsed_less_than,conv_math_str)
            conv_math_str=greater_than_pat.sub(parsed_greater_than,conv_math_str)
            
            conv_math_str=inline_begin+conv_math_str+inline_end

        self.conv_math_str=conv_math_str
        
    def sub_math_no(self,pre_parse_str):
        # 「inline_math_数字」と置換する
        return inline_dollar_pat.sub(
            self.rpl_str,
            pre_parse_str,
            count=1)
    
    def sub_math_str(self,post_parse_str):
        # 置換した「inline_math_数字」をパースした元のインライン数式で置換する。
        return re.sub(
            self.rpl_str,
            repr(self.conv_math_str)[1:-1],
            post_parse_str)

# mdモジュールのパーサー(表変換機能付き)
md_parser=md.Markdown(extensions=['tables'])

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


def parse_plain_block(plain_block,svg=False):
    """
    インライン数式を一旦退避させて、
    mdモジュールで変換した後、
    退避させていたインライン数式を(はてな記法に変換した上で)
    変換後の文字列に戻す。
    """
    
    # 標準ブロックをすべて結合し、文字列にする
    plain_str="".join(plain_block)
    # インライン数式をすべて探し、
    #「inline_math_数字」と置換する。
    match_results=inline_dollar_pat.findall(plain_str)
    match_num=len(match_results)
    parsing_math_list=[]
    for i in range(match_num):
        # InlineMathオブジェクトを生成する
        parsing_math_list.append( InlineMath(
            inline_math_str=match_results[i],
            match_no=i,
            svg=svg) )
        plain_str=parsing_math_list[-1].sub_math_no(plain_str)

    # 数式を置換した文字列をmdモジュールでパースする。
    parsed=md_parser.convert(plain_str)
    
    parsed=h3tag_begin_pat.sub(h4tag_begin,parsed)
    parsed=h3tag_end_pat.sub(h4tag_end,parsed)
    
    parsed=h2tag_begin_pat.sub(h3tag_begin,parsed)
    parsed=h2tag_end_pat.sub(h3tag_end,parsed)
    
    # 置換した「inline_math_数字」をパースした元のインライン数式で置換する。
    for i in range(match_num):
        parsed=parsing_math_list[i].sub_math_str(parsed)

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

def parse_block_list(md_block_list,svg=False):
    """
    ブロックのリストそれぞれをパースする
    """
    parsed_list=[]

    for block in md_block_list:
        if block[0] == "plain_block":
            parsed_list.append( parse_plain_block(block[1],svg=svg))
        elif block[0] == "math_block":
            parsed_list.append( parse_math_block(block[1],svg=svg))
    return parsed_list

        
def parse_md_to_hatena(md_path,svg=False):
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
    parsed_list=parse_block_list(md_block_list,svg=svg)

    # 保存する
    hatena_path=Path(md_path.stem+"_hatena.html")
    hatena_path.write_text("\n".join(parsed_list),encoding='utf-8')