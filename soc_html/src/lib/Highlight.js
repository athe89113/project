// highlight.js
import Vue from 'vue'
import Hljs from 'highlight.js'
import 'src/assets/css/googlecode.css'
let Highlight = {}
Highlight.install = function (Vue, options) {

  Vue.directive('highlight',{
    // 当绑定元素插入到 DOM 中。
    bind: function () {
      let blocks = this.el.querySelectorAll('pre code');
      blocks.forEach((block) => {
        Hljs.highlightBlock(block)
      })
    },
    update: function (value) {
      if(value){
        let blocks = this.el.querySelectorAll('pre code');
        blocks.forEach((block) => {
          block.innerHTML="<code class='sql'>"+value+"</code>";
          Hljs.highlightBlock(block)
        })
      }else{
        let blocks = this.el.querySelectorAll('pre code');
        blocks.forEach((block) => {
          Hljs.highlightBlock(block)
        })
      }
    },
  })
}
export default Highlight

