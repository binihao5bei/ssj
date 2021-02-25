var isClickedGetImeBtn = false;
var strImeInfo = "";

if ("WebSocket" in window) {} else {
    alert("浏览器不支持 WebSocket!");
}

var ws = new WebSocket("ws://localhost:9118");
if (ws.readyState == WebSocket.CONNECTING) {
    layer.msg('WebSocket正在连接...');
}

ws.onerror = function(event) {
    layer.msg('WebSocket发生错误');
};
ws.onopen = function() {
    // SetOutputMode:设置上屏方式 0:shift+insert; 1:ctrl+v; 2:websocket message;
    //ws.send("SetOutputMode,2");
    layer.msg('WebSocket连接成功');
};

ws.onmessage = function(evt) {
    console.debug("WebSocket message received:", event);
    var received_msg = evt.data;
    if (received_msg == "") {
        console.log("null info .");
    }
    console.log(received_msg);
    if (received_msg == "ImeError") {
        console.log("Ime Error");
    } else {
        if (isClickedGetImeBtn) {
            strImeInfo += received_msg;
            document.getElementById("strImeInfo").value=strImeInfo
            isClickedGetImeBtn = false;
        } else {
            var focusElement = document.activeElement;
             console.log("Ime Error" + focusElement.tagName);
            if (focusElement.tagName == "INPUT") {
                console.log(focusElement.value);
                focusElement.value += received_msg;
            }
        }
    }
};

ws.onclose = function() {
    layer.msg('WebSocket连接已关闭，请检查一下服务是否已开启!');
};

const IME_WIDTH = 1080;
const IME_HEIGHT = 388;

function IsWsConnected() {
    if (ws.readyState == WebSocket.OPEN) {
        return true;
    }

    return false;
}

function MoveImeToCenter() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,MoveImeToCenter失败.");
        return;
    }
    var strMoveInfo = "MoveIme,";
    var width = screen.width;
    width = width - IME_WIDTH;
    width = width / 2.0;
    strMoveInfo += width;
    strMoveInfo += ",";
    var height = screen.height;
    height -= IME_HEIGHT;
    strMoveInfo += height;
    ws.send(strMoveInfo);
}

function Py26Focus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,Py26Focus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_py26");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function Py9Focus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,Py9Focus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_py9");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function SignatureFoucus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,SignatureFoucus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_signature");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function HandInputHalfFoucus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,SignatureFoucus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_handInput_V_Half");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function HandInputFullFoucus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,SignatureFoucus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_handInput_V_Full");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}


function KeyboardvoiceFoucus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,SignatureFoucus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_voice");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function KeyboardsymbolFoucus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,SignatureFoucus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_symbol");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function UnFocus() {
    ws.send("HideIme");
}

function En26Focus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,En26Focus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_en26");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function NumberFocus() {
    if (!IsWsConnected()) {
        console.log("WebSocket未连接,NumberFocus 失败");
        return;
    }
    ws.send("SetCurrentLayout,Keyboard_number");
    ws.send("ShowIme");
    MoveImeToCenter();
    document.getElementById("text_input").focus();
}

function ButtonShowIme() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    ws.send("ShowIme");
    MoveImeToCenter();
}

function ButtonHideIme() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    ws.send("HideIme");
}

function handleJianFanClick(obj) {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,设置无效');
        return;
    }
    console.log(obj.options.selectedIndex);
    var traditinonInfo = "SetTraditionInput,";
    if (obj.options.selectedIndex==0) {

        traditinonInfo+=document.getElementById("jian").value;
        ws.send(traditinonInfo);
        layer.msg('简体输入已经开启');
    } else {
        traditinonInfo+=document.getElementById("fan").value;
        ws.send(traditinonInfo);
        layer.msg('繁体输入已经开启');
    }
}

function handleOutputModeClick(obj) {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,设置无效');
        return;
    }
    var outputModeInfo = "SetOutputMode,";
    outputModeInfo += obj.value;
    console.log(outputModeInfo);
    ws.send(outputModeInfo);
}

function ButtonGetImeVersion() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    strImeInfo = "版本号：";
    ws.send("GetImeVersion");
    isClickedGetImeBtn = true;
}

function ButtonGetImeSkinPath() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    strImeInfo = "默认皮肤路径：";
    ws.send("GetImeSkinPath");
    isClickedGetImeBtn = true;
}

function ButtonGetCurrentLayout() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    strImeInfo = "当前键盘布局：";
    ws.send("GetCurrentLayout");
    isClickedGetImeBtn = true;
}

function ButtonGetCellDictVersion() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    strImeInfo = "细胞词库版本号：";
    ws.send("GetCellDictVersion");
    isClickedGetImeBtn = true;
}

function ButtonGetCellDictName() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    strImeInfo = "细胞词库名字：";
    ws.send("GetCellDictName");
    isClickedGetImeBtn = true;
}

function ButtonGetCellDictWordCount() {
    if (!IsWsConnected()) {
        layer.msg('WebSocket未连接,接口访问无效');
        return;
    }
    strImeInfo = "细胞词库词条数：";
    ws.send("GetCellDictWordCount");
    isClickedGetImeBtn = true;
}

function ButtonGetmoveIme() {
    if (!IsWsConnected()) {
        layer.msg('weiz');
        return;
    }
    var x=document.getElementById("x").value;
    var y=document.getElementById("y").value;
    var z="MoveIme,"+x+","+y;
    ws.send(z);

}
function Show() {
    var reader = new FileReader();
    reader.onload = function()
    {
        document.getElementById("auth").value = this.result;

    }
    var f = document.getElementById("filePicker").files[0];
    reader.readAsText(f);
}