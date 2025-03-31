// 修改前端应用，使用原始书卷顺序
let bibleData = {};
let bookOrder = [];

// 获取DOM元素
const bookSelect = document.getElementById('bookSelect');
const chapterSelect = document.getElementById('chapterSelect');
const verseSelect = document.getElementById('verseSelect');
const verseReference = document.getElementById('verseReference');
const verseText = document.getElementById('verseText');

// 初始化应用
async function initApp() {
    try {
        // 加载书卷顺序
        const bookOrderResponse = await fetch('book_order.json');
        bookOrder = await bookOrderResponse.json();
        console.log('加载的书卷数量:', bookOrder.length);
        console.log('书卷顺序示例:', bookOrder.slice(0, 10));
        
        // 加载圣经数据
        const bibleDataResponse = await fetch('bible_data.json');
        bibleData = await bibleDataResponse.json();
        
        // 填充书卷下拉菜单
        populateBookSelect();
        
        // 添加事件监听器
        bookSelect.addEventListener('change', onBookChange);
        chapterSelect.addEventListener('change', onChapterChange);
        verseSelect.addEventListener('change', onVerseChange);
    } catch (error) {
        console.error('加载圣经数据时出错:', error);
        verseText.textContent = '加载圣经数据时出错，请刷新页面重试。';
    }
}

// 填充书卷下拉菜单，使用原始书卷顺序
function populateBookSelect() {
    bookSelect.innerHTML = '<option value="">请选择书卷...</option>';
    
    // 使用原始书卷顺序
    bookOrder.forEach(book => {
        if (bibleData[book]) { // 确保书卷在数据中存在
            const option = document.createElement('option');
            option.value = book;
            option.textContent = book;
            bookSelect.appendChild(option);
        }
    });
    
    // 检查下拉菜单中的选项数量
    console.log('下拉菜单中的选项数量:', bookSelect.options.length);
}

// 当书卷选择改变时
function onBookChange() {
    const selectedBook = bookSelect.value;
    console.log('选择的书卷:', selectedBook);
    
    // 重置章节和经文选择
    chapterSelect.innerHTML = '<option value="">请选择章节...</option>';
    verseSelect.innerHTML = '<option value="">请选择经节...</option>';
    verseText.textContent = '';
    verseReference.textContent = '请选择一个经节';
    
    // 如果没有选择书卷，禁用章节选择
    if (!selectedBook) {
        chapterSelect.disabled = true;
        verseSelect.disabled = true;
        return;
    }
    
    // 检查选择的书卷是否存在于数据中
    if (!bibleData[selectedBook]) {
        console.error('书卷数据不存在:', selectedBook);
        verseText.textContent = `错误: 找不到书卷 "${selectedBook}" 的数据`;
        chapterSelect.disabled = true;
        verseSelect.disabled = true;
        return;
    }
    
    // 填充章节下拉菜单
    const chapters = Object.keys(bibleData[selectedBook]).sort((a, b) => parseInt(a) - parseInt(b));
    console.log(`${selectedBook} 的章节数量:`, chapters.length);
    
    chapters.forEach(chapter => {
        const option = document.createElement('option');
        option.value = chapter;
        option.textContent = chapter;
        chapterSelect.appendChild(option);
    });
    
    // 启用章节选择
    chapterSelect.disabled = false;
    verseSelect.disabled = true;
}

// 当章节选择改变时
function onChapterChange() {
    const selectedBook = bookSelect.value;
    const selectedChapter = chapterSelect.value;
    console.log('选择的章节:', selectedBook, selectedChapter);
    
    // 重置经文选择
    verseSelect.innerHTML = '<option value="">请选择经节...</option>';
    verseText.textContent = '';
    verseReference.textContent = '请选择一个经节';
    
    // 如果没有选择章节，禁用经文选择
    if (!selectedChapter) {
        verseSelect.disabled = true;
        return;
    }
    
    // 检查选择的章节是否存在于数据中
    if (!bibleData[selectedBook][selectedChapter]) {
        console.error('章节数据不存在:', selectedBook, selectedChapter);
        verseText.textContent = `错误: 找不到 ${selectedBook} ${selectedChapter}章 的数据`;
        verseSelect.disabled = true;
        return;
    }
    
    // 填充经文下拉菜单
    const verses = Object.keys(bibleData[selectedBook][selectedChapter]).sort((a, b) => parseInt(a) - parseInt(b));
    console.log(`${selectedBook} ${selectedChapter}章 的经文数量:`, verses.length);
    
    verses.forEach(verse => {
        const option = document.createElement('option');
        option.value = verse;
        option.textContent = verse;
        verseSelect.appendChild(option);
    });
    
    // 启用经文选择
    verseSelect.disabled = false;
}

// 当经文选择改变时
function onVerseChange() {
    const selectedBook = bookSelect.value;
    const selectedChapter = chapterSelect.value;
    const selectedVerse = verseSelect.value;
    console.log('选择的经文:', selectedBook, selectedChapter, selectedVerse);
    
    // 如果没有选择经文，清空显示
    if (!selectedVerse) {
        verseText.textContent = '';
        verseReference.textContent = '请选择一个经节';
        return;
    }
    
    // 检查选择的经文是否存在于数据中
    if (!bibleData[selectedBook][selectedChapter][selectedVerse]) {
        console.error('经文数据不存在:', selectedBook, selectedChapter, selectedVerse);
        verseText.textContent = `错误: 找不到 ${selectedBook} ${selectedChapter}:${selectedVerse} 的数据`;
        return;
    }
    
    // 显示选中的经文
    const verse = bibleData[selectedBook][selectedChapter][selectedVerse];
    verseText.textContent = verse;
    verseReference.textContent = `${selectedBook} ${selectedChapter}:${selectedVerse}`;
}

// 初始化应用
document.addEventListener('DOMContentLoaded', initApp);
