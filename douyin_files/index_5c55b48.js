__M.define("douyin_falcon:component/common/openBrowser/index",function(require,exports,module){"";function _classCallCheck(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function _defineProperties(e,n){for(var r=0;r<n.length;r++){var o=n[r];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function _createClass(e,n,r){return n&&_defineProperties(e.prototype,n),r&&_defineProperties(e,r),e}var tmpRenderer=function(obj){{var __p="";Array.prototype.join}with(obj||{})__p+='<div class="open-browser">\n    <div class="open-browser-content">\n        <h5>链接打不开？</h5>\n        <p>请点击右上角</p>\n        <p>选择在“<span>浏览器</span>”中打开</p>\n        <div class="guider"></div>\n    </div>\n</div>';return __p},BrowserOpen=function(){function e(){_classCallCheck(this,e),this.el=null}return _createClass(e,[{key:"open",value:function(){var e=this;if(this.el)return void this.el.show(200);var n=document.createElement("div");n.innerHTML=tmpRenderer(),document.body.appendChild(n),this.el=$(".open-browser"),this.el.show(200);this.el.click(function(n){n.target==e.el[0]&&e.close()})}},{key:"close",value:function(){this.el.hide(200)}}]),e}();module.exports=BrowserOpen});