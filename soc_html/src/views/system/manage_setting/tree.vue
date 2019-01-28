<template>
  <div class="tree-box">
    <ul v-for="per in options" v-show="showSelf" class="treeList">
      <li class="pos-r">
        <p v-bind:style="{marginLeft: (per.re * 72 - 102) + 'px' }" v-bind:class="[per.re==1 ? 'm-0' : '']">
          <!--<span class="menuLine" v-if="per.re>1" v-bind:style="{marginLeft: (per.re * 20) + 'px' }">-->
          <!--<span class="middle"></span>-->
          <!--</span>-->
          <span class="ver-line mid" v-if="per.re>1 && $index!=options.length-1"></span>
          <span class="ver-line last" v-if="per.re>1 && $index==options.length-1 && !per.show"></span>
          <span class="ver-line last-show" v-if="per.re>1 && $index==options.length-1 && per.show"></span>
          <span class="hor-line" v-if="per.re>1"></span>
          <span @click="showChildren(per)">
            <i class="ys-icon ys-primary-color text-cursor verticalM" v-bind:class="[per.show? 'icon-minus-box' : 'icon-plus-box' ]"
               v-if="per.children.length>0"></i>
          </span>
          <span>
            <!--<input type="checkbox" v-model="per.enable" @click="emitCheck(per)">-->
            <checkbox @ys-click="emitCheck(per)" :show.sync="per.enable" :auto-set="false"></checkbox>
          </span>
          <span class="m-l-5 ys-info-color verticalM">{{per.name}}</span>
        </p>
        <permissions-tree :options="per.children" :show-self="per.show"></permissions-tree>
      </li>
    </ul>
  </div>
</template>
<style scoped>
  .hor-line{
    height:1px;
    width:26px;
    background:#7e9fd0;
    display: inline-block;
    vertical-align: middle;
    margin-right:3px;
  }
  .ver-line{
    position:absolute;
    width:1px;
    background:#7e9fd0;
    display: inline-block;
  }
  .ver-line.first{
    bottom:0px;
    height:50%!important;
  }
  .ver-line.mid{
    top:0px;
    height:100%!important;
  }
  .ver-line.last{
    top:0px;
    height:50%!important;
  }
  .ver-line.last-show{
    top:0px;
    height:16px;
  }
  .treeList{}
  .treeList li{
    padding:10px
  }
  .menuLine{
    display: inline-block;
    width:35px;
    position: relative;
    vertical-align: middle;
  }
  .menuLine>span{
    display: inline-block;
    position:absolute;
    background:#5373b1;
  }
  .menuLine .top{
    top:0px;
    left:0px;
    width:1px;
    height:18px;
  }
  .menuLine .bottom{
    bottom:0px;
    left:0px;
    width:1px;
    height:18px;
  }
  .menuLine .middle{
    bottom:0px;
    left:1px;
    width:25px;
    height:1px;
  }
</style>
<script>
  export default {
    name: 'permissions-tree',
    props: {
      options: Array,
      'show-self': {
        default: true
      },
    },
    events: {
      showChildrenEvent: function (data) {
        var self = this
        if(data.show){
          return
        }
        this.options.forEach(function (option) {
          if(option.parent_id==data.id){
            option.show=data.show
            self.showSelf=data.show
            self.$broadcast('showChildrenEvent', {id: option.permission_id, show: data.show})
          }
        })
      },
      editChildrenEvent: function (data) {
        var self = this
        this.options.forEach(function (option) {
          if(option.parent_id==data.id){
            option.enable=data.enable
            option.show = true
            let eData = {id:option.id, enable: option.enable}
            self.$dispatch('edit', eData)
            self.showSelf=true
            self.$broadcast('editChildrenEvent', {id: option.permission_id, enable: data.enable})
          }
        })
      }
    },
    data () {
      return {
        show: false
      }
    },
    ready: function () {


    },

    methods: {
      showChildren (per) {
        per.show = !per.show
        this.$broadcast('showChildrenEvent', {id: per.permission_id, show: per.show})
      },
      emitCheck(per) {
        per.enable = !per.enable
        per.show=true
        let data = {id:per.id, enable: per.enable}
        this.$dispatch('edit', data)
        this.$broadcast('editChildrenEvent', {id: per.permission_id, enable: per.enable})
      }
    },
    components: {}

  }
</script>