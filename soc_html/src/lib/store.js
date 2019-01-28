import Vue from 'vue'
import Vuex from 'vuex'

// 告诉 vue “使用” vuex
Vue.use(Vuex)

const state = {
  idc:{
    id:0,
    name:""
  },
  user:{
    package:{
      asset:{},
      ddos:{},
      hids:{},
      monitor:{},
      scan:{},
      waf:{}
    },
    menu:{
      default:{},
    }
  },
  menu:{},
  fromLogin:false,
  curDomain:{},
  domainList:{
    checkin:[],
    no_checkin:[]
  },
  cartNum:0,
  orderNum:0,
  version: {
    version: ''
  },
  curTransTask:{},
  curWorkFlow:{},
}

const mutations = {
  // mutation 的第一个参数是当前的 state
  // 你可以在函数里修改 state
  CHANGE (state, newId,newName) {
    state.idc.id = newId
    state.idc.name = newName
  },
  changeUser(state,newUserData){
    state.user=newUserData
  },
  changeDomain(state,newDomainData){
    state.curDomain=newDomainData
  },
  changeDomainList(state,newDomainList){
    state.domainList=newDomainList
  },
  changeCartNum(state,newNum){
    state.cartNum=newNum
  },
  changeOrderNum(state,newNum){
    state.orderNum=newNum
  },
  changeMenu(state,newMenu){
    state.menu=newMenu
  },
  changeFromLogin(state,newStatus){
    state.fromLogin=newStatus
  },
  changeVersion(state,newVersion){
    state.version=newVersion
  },
  changeTransTask(state,newTransTask){
    state.curTransTask=newTransTask
  },
  changeWorkFlow(state,newWorkFlow){
    state.curWorkFlow=newWorkFlow
  },
}

// 整合初始状态和变更函数，我们就得到了我们所需的 store
// 至此，这个 store 就可以连接到我们的应用中
export default new Vuex.Store({
  state,
  mutations
})