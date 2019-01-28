<template>
  <div>
    <table class="ys-table">
      <thead>
        <tr>
          <th>告警联系人</th>
          <th>邮件</th>
          <th>短信</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="list in userData">
          <td>{{list.username}}</td>
          <td><checkbox :show.sync="list.emailStatus"></checkbox></td>
          <td><checkbox :show.sync="list.phoneStatus"></checkbox></td>
        </tr>  
      </tbody>  
    </table>
  </div>  
</template>
<style scoped>

</style>
<script>
export default {
  name: "notify",
  data () {
    return {
      userData:[],
    }
  },
  ready () {  
    this.getWarnUserData();
  },
  methods:{
    getWarnUserData(){
      this.$http.get('/api/message/user_list').then(function (response) {
        let data = response.data.data;
        for(let x in data){
          data[x].emailStatus=false;
          data[x].phoneStatus=false;
        }
        this.userData=data;
      }, function (response) {
          Api.user.requestFalse(response,this);
      })
    },
  }
}
</script>