<template>
  <div class="ys-box">
    <div class="ys-box-con">
      <div class="tool-box">
        <div class="fLeft d-i-b">
          <button class="ys-btn" @click="addIdcSave">
            <i class="ys-icon icon-add-circle"></i>添加机房

          </button>
        </div>
        <div class="fRight d-i-b">
          <ys-select :option="filterLocations"
                     :width="150"
                     :selected.sync="tableFilter.location_id"
                     :filter="true"
                     @change=""></ys-select>
          <ys-select :option="filterIspLines"
                     :width="100"
                     :selected.sync="tableFilter.isp_line"
                     :filter="true"
                     @change="tableRe()"></ys-select>
          <div class="ys-search d-i-b m-l-10">
            <input type="text" placeholder="输入关键词查询"
                   v-model="searchValue"
                   @blur="tableRe()"
                   @keyup.enter="tableRe()"
                   class="ys-input" style="width:180px;"/>
            <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
          </div>
        </div>
      </div>
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th></th>
          <th></th>
          <th class="textL">IDC名称</th>
          <th>位置</th>
          <th>ISP线路</th>
          <th>带宽</th>
          <th>机柜使用率</th>
          <th class="textC" style="width: 120px;">操作</th>
        </tr>
        </thead>
        <tbody v-for="list in tableList">
        <tr class="odd" v-bind:class="[curEditId == list.id ? 'on' : '' ]">
          <td class="detail">
              <span @click="showDetail(list.id)">
                <i class="ys-icon" v-bind:class="[curDetailId == list.id ? 'icon-downlist-up' : 'icon-downlist' ]"></i>
              </span>
          </td>
          <td class="check">
            <checkbox></checkbox>
          </td>
          <td class="textL"><span>{{list.name}}</span></td>
          <td>北京(beijing)</td>
          <td>中国移动</td>
          <td>300</td>
          <td>
            <percent :data="list.rack_percent"></percent>
          </td>
          <td class="operate">
            <tooltip :content="'编辑'" :delay="1000">
              <a @click="edit(list.id)"><i class="ys-icon icon-edit"></i></a>
            </tooltip>
            <ys-poptip confirm
                       title="您确认此选项吗？"
                       :placement="'left'"
                       @on-ok=""
                       @on-cancel="">
              <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
            </ys-poptip>
          </td>
        </tr>
        <tr class="detail" v-bind:class="[curDetailId == list.id ? 'open' : '' ]">
          <td colspan="8">
            <div class="detail-info">
              <div class="p-15">
                <p>
                  印着画好腮红深入矿井视察 在与矿工 动静对望时 没再深望 随行的记着 抽泣着 向民众播报着澄缺的实情
                  错误心跳早上他非脱落咖啡四季风尚
                </p>
                <p class="m-t-5">
                  印着画好腮红深入矿井视察 在与矿工 动静对望时 没再深望 随行的记着 抽泣着 向民众播报着澄缺的实情
                  错误心跳早上他非脱落咖啡四季风尚
                </p>
                <p class="m-t-5">
                  印着画好腮红深入矿井视察 在与矿工 动静对望时 没再深望 随行的记着 抽泣着 向民众播报着澄缺的实情
                  错误心跳早上他非脱落咖啡四季风尚
                </p>
              </div>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
      <table-data :url='tableUrl'
                  :data.sync="tableList"
                  v-ref:table></table-data>
      <div class="ys-table-more">
        <checkbox :text="'全选'"></checkbox>
        <ys-poptip>
          <a class="m-l-10 verticalM">操作</a>
        </ys-poptip>
        <ys-poptip>
          <a class="m-l-10 verticalM">操作</a>
        </ys-poptip>
      </div>
      <div style="margin-top:100px;">
        <step-all :title="'aaaaa'" :step="1">
          <p><span class="m-r-8">选择域名</span><input class="ys-input"></p>
        </step-all>
      </div>
      <div>
        <guides :step="stepData" :cur="curStep">
          <div slot="content">
            <div v-if="curStep==1">
              <p><span class="m-r-8">选择域名</span><input class="ys-input"></p>
              <p class="m-t-10">
                <button class="ys-btn" @click="curStep=2">下一步</button>
              </p>
            </div>
            <div v-if="curStep==2">
              <p><span class="m-r-8">选择域名</span><input class="ys-input"></p>
              <p><span class="m-r-8">选择域名</span><input class="ys-input"></p>
              <p><span class="m-r-8">选择域名</span><input class="ys-input"></p>
              <p class="m-t-10">
                <button class="ys-btn" @click="curStep=1">上一步</button>
              </p>
              <p class="m-t-10">
                <button class="ys-btn" @click="curStep=3">下一步</button>
              </p>
            </div>
            <div v-if="curStep==3">
              <p><span class="m-r-8">选择选择域名选择域名域名</span><input class="ys-input"></p>
              <p class="m-t-10">
                <button class="ys-btn" @click="curStep=2">上一步</button>
              </p>
            </div>
          </div>
        </guides>
      </div>
    </div>
  </div>
  <aside :show.sync="showConfigStatus"
         :header="configHead"
         :left="'auto'"
         :width="'500px'">
    <validator name="valCluster" @valid="onConfigValid = true" @invalid="onConfigValid = false">
      <div>
        <table class="ys-form-table m-t-10">
          <tr>
            <td>名称</td>
            <td>
              <ys-valid>
                <input class="ys-input"
                       placeholder="名称"
                       v-model=""/>
              </ys-valid>
            </td>
          </tr>
          <tr>
            <td>列表选择</td>
            <td>
              <ys-valid>
                <ys-select :option="filterIspLines"
                           :selected.sync="tableFilter.isp_line"></ys-select>
              </ys-valid>
            </td>
          </tr>
          <tr>
            <td>防御带宽</td>
            <td>
              <ys-valid>
                <input class="ys-input"
                       placeholder="防御带宽"
                       v-model=""/>
              </ys-valid>
            </td>
          </tr>
          <tr>
            <td>IP地址</td>
            <td>
              <ys-valid>
                <input class="ys-input"
                       placeholder="IP地址"
                       v-model=""/>
              </ys-valid>
            </td>
          </tr>
          <tr>
            <td>字数长一</td>
            <td>
              <span class="m-r-24"><checkbox :text="'青松产品'"></checkbox></span>
              <span><checkbox :text="'云松产品'"></checkbox></span>
            </td>
          </tr>
          <tr>
            <td>字数长一</td>
            <td>
              <radio :list="radioData" :value.sync="curRadio"></radio>
            </td>
          </tr>
          <tr>
            <td>字数长一点再长再长</td>
            <td>
              <ys-valid>
                <input class="ys-input"
                       placeholder="字数长一点再长再长"
                       v-model=""/>
              </ys-valid>
            </td>
          </tr>
        </table>
      </div>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" @click="">确定</button>
        <button class="ys-btn ys-btn-white" @click="">取消</button>
      </div>
    </validator>
  </aside>
</template>
<style scoped>

</style>
<script>

  export default {
    name: "example",
    data() {
      return {
        tableUrl: "/api/idc/dts",
        tableList: "",
        tableFilter: {
          location_id: {"id": "", "name": "全部位置"},
          isp_line: {"id": "", "name": "全部线路"}
        },
        filterLocations: [],
        filterIspLines: [],
        searchValue: "",
        showConfigStatus: false,
        configHead: "侧边栏标题文字",

        curEditId: 0,
        curDetailId: 0,

        radioData: [
          {id: 1, text: "猴子"},
          {id: 2, text: "猿猴"},
          {id: 3, text: "大猩猩"},
          {id: 4, text: "milo"},
        ],
        curRadio: 1,
        curStep: 1,
        stepData: [
          {step: 1, before: "第一步内容", after: "完成第一步"},
          {step: 2, before: "第二步内容", after: "完成第二步"},
          {step: 3, before: "第三步内容", after: "完成第三步"},
        ]
      }
    },
    ready: function () {

    },
    methods: {
      showMiniLoad(){
        this.loadMini = true;
      },
      tableRe(){
        this.$refs.table.Re()
      },
      edit(id){
        this.curEditId = id;//设置当前编辑id
        this.curDetailId = "";//把当前展示详情ID置为空
        this.showConfigStatus = true;//弹出右侧滑出界面
      },
      showDetail(id){
        this.curEditId = "";//设置当前编辑ID为空
        //如果curEditId和此条id相同,就关闭,否则就展示详情
        if (this.curDetailId == id) {
          this.curDetailId = ""
        } else {
          this.curDetailId = id;
        }
      },
      addIdcSave(){
        this.showConfigStatus = true;
      }

    },
    components: {}
  }
</script>
