<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="tree">
        <ul>
          <li>
            <tooltip :placement="'right'" :content="nodeTopo.ip">
              <span v-bind:class="[nodeTopo.status == 0 || nodeTopo.status == 2 ? 'offline' : '' ]">{{nodeTopo.name}}</span>
            </tooltip>
            <ul>
              <li v-for="child in nodeTopo.children">
                <tooltip :placement="'right'" :content="child.ip">
                  <span v-bind:class="[child.status == 0 || child.status == 2 ? 'offline' : '' ]">{{child.name}}</span>
                </tooltip>
                <ul>
                  <li v-for="gChild in child.children">
                    <tooltip :placement="'bottom'" :content="gChild.ip">
                      <span v-bind:class="[gChild.status == 0 || gChild.status == 2 ? 'offline' : '' ]">{{gChild.name}}<i></i></span>
                    </tooltip>
                  </li>
                </ul>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .offline {
    color: #e96157;
  }
  .tree ul {
    position: relative;
    padding: 20px 0;
    white-space: nowrap;
    margin: 0 auto;
    text-align: center;

  }

  .tree ul::after {
    content: '';
    display: table;
    clear: both;
  }

  .tree li {
    display: inline-block;
    vertical-align: top;
    text-align: center;
    list-style-type: none;
    position: relative;
    padding: 20px .5em 0 .5em;

  }

  .tree li::before,
  .tree li::after {
    content: '';
    position: absolute;
    top: 0;
    right: 50%;
    border-top: 1px solid rgba(74,146,255,0.4);
    width: 50%;
    height: 20px;
  }

  .tree li::after {
    right: auto;
    left: 50%;
    border-left: 1px solid rgba(74,146,255,0.4);
  }

  .tree li:only-child::after,
  .tree li:only-child::before {
    display: none;
  }

  .tree li:only-child {
    padding-top: 0;
  }

  .tree li:first-child::before,
  .tree li:last-child::after {
    border: 0 none;
  }

  .tree li:last-child::before {
    border-right: 1px solid rgba(74,146,255,0.4);
    border-radius: 0 5px 0 0;
  }

  .tree li:first-child::after {
    border-radius: 5px 0 0 0;
  }

  .tree ul ul::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    border-left: 1px solid rgba(74,146,255,0.4);
    width: 0;
    height: 20px;
  }

  .tree li span {
    border: 1px solid rgba(74,146,255,0.4);
    background-color: rgba(74,146,255,0.1);
    padding: 15px 30px;
    text-decoration: none;
    display: inline-block;
    border-radius: 3px;
    position: relative;
    top: 1px;
    cursor:pointer;
  }

  .tree li span:hover,
  .tree li span:hover + ul li span {
    /*background: #e9453f;*/
    /*color: #fff;*/
    border: 1px solid #4a92ff;
  }

  .tree li span:hover + ul li::after,
  .tree li span:hover + ul li::before,
  .tree li span:hover + ul::before,
  .tree li span:hover + ul ul::before {
    border-color: #4a92ff;
  }

</style>
<script>
  import Api from 'src/lib/api'
  export default {
    name: "node-state-topo",
    data(){
      return {
        nodeTopo: {}
      }
    },
    ready: function () {
      this.getNodeTopo()
    },
    methods: {
      getNodeTopo(){
        this.$http.get('/api/system/nodes/topo').then(function (response) {
          if (response.data.status == 200) {
            this.nodeTopo = response.data.data;
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      }
    },
    components: {
    }
  }
</script>
