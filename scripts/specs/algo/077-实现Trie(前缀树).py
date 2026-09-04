from scripts.algo_gen import frame

PROBLEM = {
    "id": 77,
    "title": "实现Trie(前缀树)",
    "diff": "medium",
    "tags": ["Trie"],
    "leetcode": 208,
    "origin": "https://leetcode.cn/problems/implement-trie-prefix-tree/",
    "why": "Trie 用「节点 = 字符」的多叉树存储单词，共享公共前缀。每个节点存子节点指针数组 + is_end 标记，插入/查找/前缀判断都是 O(单词长度)。",
    "desc": """<p>实现 Trie（前缀树），支持 <code>insert(word)</code>、<code>search(word)</code>（单词是否存在）、<code>startsWith(prefix)</code>（是否有该前缀）。</p>
<p><strong>示例：</strong><br><code>insert("apple")</code>；<code>search("apple")→true</code>；<code>search("app")→false</code>；<code>startsWith("app")→true</code></p>""",
    "frames": [
    frame("① 插入 apple、app：共享前缀 a-p-p", "drawTable", headers=["单词", "路径"], rows=[["apple", "a→p→p→l→e(终)"], ["app", "a→p→p(终)"]], width=500, height=140),
    frame("② 节点结构：children[26] + is_end", "drawTable", headers=["节点", "children", "is_end"], rows=[["'p'", "a~z 子指针", "false"], ["'e'", "…", "true"]], width=500, height=140),
    ],
    "conclusion": "逐字符向下走，最后一个字符的 is_end 决定「是完整单词还是仅前缀」。",
    "py": """class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False
    def insert(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True
    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end
    def startsWith(self, prefix):
        return self._walk(prefix) is not None
    def _walk(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node""",
    "java": """class Trie {
    Trie[] next = new Trie[26];
    boolean isEnd;
    public void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) node.next[i] = new Trie();
            node = node.next[i];
        }
        node.isEnd = true;
    }
    public boolean search(String word) {
        Trie n = walk(word);
        return n != null && n.isEnd;
    }
    public boolean startsWith(String prefix) { return walk(prefix) != null; }
    Trie walk(String s) {
        Trie node = this;
        for (char c : s.toCharArray()) {
            if (node.next[c - 'a'] == null) return null;
            node = node.next[c - 'a'];
        }
        return node;
    }
}""",
    "time": "插入/查找/前缀均 O(len)",
    "space": "O(节点数 × 字符集)",
    "pitfalls": [["is_end 与前缀区分", "search 要求 is_end=true，startsWith 只要求路径存在"], ["字符下标", "小写字母用 c-'a' 映射到 0..25，哈希表版无需关心"]],
    "selfcheck": [["search(\"app\") 为何 false？", "路径 a-p-p 存在但 'p' 不是插入时的终点（is_end=false），所以只是前缀不是单词。"], ["Trie 的典型应用？", "自动补全、拼写检查、IP 路由最长前缀匹配、词频统计。"]],
}
