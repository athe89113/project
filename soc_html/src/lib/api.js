exports.user = {
  //检查登陆状态，如果未登录跳转到登陆页面
  checkLogon: function(transition) {
    let token = localStorage.getItem('current_user') || sessionStorage.getItem('current_user')
    if (transition.to.auth && (!token || token === null)) { // need to auth but token is not set
      transition.redirect('/login')
    }
    transition.next()
  },
  logout: function() {
    Vue.$http.get('api/logout').then(function (response) {
      if (response.data.status === 200) {
        localStorage.removeItem("current_user");
        localStorage.removeItem("role_type");
        localStorage.removeItem("is_admin");
        sessionStorage.removeItem("current_user")
        sessionStorage.removeItem("role_type")
        sessionStorage.removeItem("is_admin")
        Vue.$router.go({name: "login"});
      } else {
      }
    },function(response){
      Api.user.requestFalse(response);
    })
  },
  requestFalse: function(response,Vue){
    if(response.status==401){
      window.location.href="/login"
    }else{
      Vue.$root.loadStatus=false;
      // Vue.$root.alertError=true;
      // Vue.$root.errorMsg="服务器访问错误";
      console.log("在平坦的路面上曲折前行");
    }
    if(response.data.code==10001){
      Vue.$root.errorMsg = response.data.msg
      Vue.$root.alertError = true
    }
    if(response.data.status==403){
      Vue.$root.errorMsg = response.data.msg
      Vue.$root.alertError = true
    }
  },
}
