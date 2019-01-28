export const changeIdc = function ({ dispatch,state},id,name) {
  dispatch('CHANGE', id,name)
}
export const changeUser = function ({ dispatch,state},data) {
  dispatch('changeUser', data)
}
export const changeDomain = function ({ dispatch,state},data) {
  dispatch('changeDomain', data)
}
export const changeDomainList = function ({ dispatch,state},data) {
  dispatch('changeDomainList', data)
}
export const changeCartNum = function ({ dispatch,state},data) {
  dispatch('changeCartNum', data)
}
export const changeOrderNum = function ({ dispatch,state},data) {
  dispatch('changeOrderNum', data)
}
export const changeMenu = function ({ dispatch,state},data) {
  dispatch('changeMenu', data)
}
export const changeFromLogin = function ({ dispatch,state},data) {
  dispatch('changeFromLogin', data)
}
export const changeVersion = function ({ dispatch,state},data) {
  dispatch('changeVersion', data)
}
export const changeTransTask = function ({ dispatch,state},data) {
  dispatch('changeTransTask', data)
}
export const changeWorkFlow = function ({ dispatch,state},data) {
  dispatch('changeWorkFlow', data)
}