import os,re
import urllib.request

# mathjax-nodeを使って
# 数式をSVGに変換するnodeのURL
url = 'http://localhost:8080/convert'
headers = {
    'Content-Type': 'text/plain',
}

def parse_math_block(math_block,style="default"):
    """
    ブロック環境の数式をパースする。
    """
    if style == "default":
        converted_mb=parse_default_mb(math_block)
    elif style == "katex":
        converted_mb=parse_katex_md(math_block)
    elif style == "svg":
        converted_mb=parse_svg_md(math_block)
    else:
        raise ValueError("invalid style string")
    return converted_mb

def parse_default_mb(math_block):
    # ブロック環境の数式の始まりと終わり
    block_begin="<div align=\"center\">[tex:\displaystyle{ "
    block_end=" }]</div>"
    # ブラケットの正規表現
    bracket_begin_pat=re.compile('\\[')
    bracket_end_pat=re.compile('\\]')
    # パース後のブラケット
    parsed_bracket_begin=r'\['
    parsed_bracket_end=r'\]'
    # 不等号の正規表現
    less_than_pat=re.compile('<')
    greater_than_pat=re.compile('>')
    # パース後の不等号
    # \\が2つなのに更にraw文字列としているのは、
    # もともと必要な\のエスケープに加え、
    # re.sub()のreple引数で使うので、
    # reple引数では\を解釈してしまうのでさらにそれをエスケープするため。
    parsed_less_than=r'\\lt '
    parsed_greater_than=r'\\gt '

    new_math_list=[block_begin]
    for i in range(1,len(math_block)-1):
        line=math_block[i].rstrip(os.linesep)
        # ブラケットをエスケープする
        line=bracket_begin_pat.sub(parsed_bracket_begin, line)
        line=bracket_end_pat.sub(parsed_bracket_end, line)
        # 不等号をHTML用不等号記号に
        line=less_than_pat.sub(parsed_less_than,line)
        line=greater_than_pat.sub(parsed_greater_than,line)
        line=re.sub(r'aligned',r'align',line)
        new_math_list.append(line)
    new_math_list.append(block_end)
    return "".join(new_math_list)

def parse_katex_md(math_block):
    # ブロック環境の数式の始まりと終わり
    block_begin="<div class=\"math-render\">"
    block_end="</div>"
    # 不等号の正規表現
    less_than_pat=re.compile('<')
    greater_than_pat=re.compile('>')
    # パース後の不等号
    parsed_less_than=r'\\lt '
    parsed_greater_than=r'\\gt '

    new_math_list=[block_begin]
    for i in range(1,len(math_block)-1):
        line=math_block[i].rstrip(os.linesep)

        # 不等号をHTML用不等号記号に
        line=less_than_pat.sub(parsed_less_than,line)
        line=greater_than_pat.sub(parsed_greater_than,line)

        new_math_list.append(line)
    new_math_list.append(block_end)
    return "".join(new_math_list)

def parse_svg_md(math_block):

    # svgの場合のブロック数式の始まりと終わり
    div_begin="<div align=\"center\">"
    div_end="</div>"

    whole_mb="".join(math_block[1:-1])
    req = urllib.request.Request(url,whole_mb.encode(),headers)
    with urllib.request.urlopen(req) as res:
        body=res.read().decode("utf-8")
        parsed_math_block = \
            div_begin + body + div_end

    return parsed_math_block

# インライン環境の数式の正規表現
inline_dollar_pat=re.compile(r'\$(.+?)\$')

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
            style="default"):
        self.inline_math_str=inline_math_str
        self.match_no=match_no
        
        #「inline_math_数字」という文字列を作成する
        self.rpl_str="{}{:0=4}".format(
            type(self).math_prefix,
            match_no)

        if style == "default":
            conv_math_str=parse_default_inline(inline_math_str)
        elif style == "katex":
            conv_math_str=parse_katex_inline(inline_math_str)
        elif style == "svg":
            conv_math_str=parse_svg_inline(inline_math_str)
        else:
            raise ValueError("invalid style string")

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

def parse_default_inline(inline_math_str):
    # ブラケットの正規表現
    bracket_begin_pat=re.compile('\\[')
    bracket_end_pat=re.compile('\\]')
    # パース後のブラケット
    parsed_bracket_begin=r'\['
    parsed_bracket_end=r'\]'
    # 不等号の正規表現
    less_than_pat=re.compile('<')
    greater_than_pat=re.compile('>')
    # パース後の不等号
    parsed_less_than=r'\\lt '
    parsed_greater_than=r'\\gt '
    # インライン環境の数式の始まりと終わり
    inline_begin=r"[tex:\displaystyle{ "
    inline_end=" }]"

    conv_math_str=inline_math_str
    # ブラケットをエスケープする
    conv_math_str=bracket_begin_pat.sub(parsed_bracket_begin, conv_math_str)
    conv_math_str=bracket_end_pat.sub(parsed_bracket_end, conv_math_str)
    # 不等号をHTML用不等号記号に
    conv_math_str=less_than_pat.sub(parsed_less_than,conv_math_str)
    conv_math_str=greater_than_pat.sub(parsed_greater_than,conv_math_str)
    
    return inline_begin+conv_math_str+inline_end

def parse_katex_inline(math_str):
    # インライン環境の数式の始まりと終わり
    inline_begin="[]$"
    inline_end="$[]"

    # 不等号の正規表現
    less_than_pat=re.compile('<')
    greater_than_pat=re.compile('>')
    # パース後の不等号
    # \\が2つなのに更にraw文字列としているのは、
    # もともと必要な\のエスケープに加え、
    # re.sub()のreple引数で使うので、
    # reple引数では\を解釈してしまうのでさらにそれをエスケープするため。
    parsed_less_than=r'\\lt '
    parsed_greater_than=r'\\gt '
    # 指数(キャレット)の正規表現
    caret_pat=re.compile('\^')
    # アンダーバーの正規表現
    under_bar_pat=re.compile('_')
    # エスケープ済み波括弧の正規表現
    curly_begin_pat=re.compile('\\\\{')
    curly_end_pat=re.compile('\\\\}')

    conv_math_str=math_str
    # 不等号をHTML用不等号記号に
    conv_math_str=less_than_pat.sub(parsed_less_than,conv_math_str)
    conv_math_str=greater_than_pat.sub(parsed_greater_than,conv_math_str)
    # キャレットの前後に空白を
    conv_math_str=caret_pat.sub(" ^ ",conv_math_str)
    # アンダーバーの前後に空白を
    conv_math_str=under_bar_pat.sub(" _ ",conv_math_str)
    # 波括弧のエスケープをさらにエスケープ
    conv_math_str=curly_begin_pat.sub(r"\\\\{",conv_math_str)
    conv_math_str=curly_end_pat.sub(r"\\\\}",conv_math_str)
    
    return inline_begin+conv_math_str+inline_end 

def parse_svg_inline(inline_math_str):
    req = urllib.request.Request(
        url,
        inline_math_str.encode(),
        headers)
    with urllib.request.urlopen(req) as res:
        conv_math_str=res.read().decode("utf-8")

    return conv_math_str