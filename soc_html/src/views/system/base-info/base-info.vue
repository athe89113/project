<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <table class="ys-form-table">
        <tr>
          <td class="ys-info-color">系统名称</td>
          <td>
            <input class="ys-input ys-input-length"
                   v-model="tableList.title"
                   placeholder="网站名称最大长度10个字符"/>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">系统域名</td>
          <td>
            <input class="ys-input ys-input-length"
                   v-model="tableList.web_domain"
                   placeholder="域名请不包括http://或https://"/>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">LOGO上传</td>
          <td>
            <div class="ys-file-input">
              <input class="ys-input ys-input-length" placeholder="选择logo文件"
                     v-model="LogoName"/>
              <i class="ys-icon icon-file ys-primary-color text-cursor"  @click="selKeylessFileFunc(2)"></i>
              <div class="form-group d-none">
                <form enctype="multipart/form-data" method="post">
                  <input id="keyless_pub" class="ys-input" type="file" @change="bindKeylessPubFile" class="form-control">
                </form>
              </div>
            </div>
          </td>
        </tr>
        <tr>
          <td></td>
          <td style="padding:4px">
            <p class="ys-info-color">LOGO文件格式为背景透明的.png文件，尺寸最大140 x 30 pt，文件最大200KB</p>
          </td>
        </tr>

        <tr>
          <td class="ys-info-color">服务电话</td>
          <td>
            <input class="ys-input ys-input-length"
                   v-model="tableList.server_phone"
                   placeholder="例如：400-8000-800"/>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">联系邮箱</td>
          <td>
            <input class="ys-input ys-input-length"
                   v-model="tableList.email"
                   placeholder="例如：admin@test.com"/>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">备案编号</td>
          <td>
            <input class="ys-input ys-input-length"
                   v-model="tableList.record_number"
                   placeholder="例如：京ICP备11111111号"/>
          </td>
        </tr>
      </table>
      <section class="m-t-20">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" @click="saveSettings()">保存基本信息</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.ys-input-length{
  width:260px;
}
</style>
<script>
  // #7e9fd0
  import { changeUser } from 'src/lib/actions'
  export default {
    name: 'base-info',
    data () {
      return {
        adminPassword: '',
        tableList: '',
        test_phone: '',
        LogoName: '',
        LogoFile: new FormData(), // 文件上传
      }
    },
    vuex: {
      actions: {
        changeUser,
      }
    },
    ready: function () {
      this.getInfo()
    },
    methods: {
      getInfo () {
        this.$http.get('/api/system/baseinfo').then(function (response) {
          if (response.data.status === 200) {
            this.tableList = response.data.data;
            this.LogoName = response.data.data.web_logo;
            this.LogoFile = new FormData(); // 文件上传
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      refresh () {
        this.$http.get('/api/profile').then(function (response) {
          this.changeUser(response.data.data)
        })
      },
      saveSettings () {
        this.LogoFile.delete('admin_password');
        this.LogoFile.delete('title');
        this.LogoFile.delete('web_domain');
        this.LogoFile.delete('record_number');
        this.LogoFile.delete('server_phone');
        this.LogoFile.delete('email');
        this.LogoFile.append('admin_password', this.adminPassword);
        this.LogoFile.append('title', this.tableList['title']);
        this.LogoFile.append('web_domain', this.tableList['web_domain']);
        this.LogoFile.append('record_number', this.tableList['record_number']);
        this.LogoFile.append('server_phone', this.tableList['server_phone']);
        this.LogoFile.append('email', this.tableList['email']);
        this.$http.put('/api/system/baseinfo', this.LogoFile).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
            this.refresh()
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      selKeylessFileFunc () {
        $('#keyless_pub').click();
      },
      bindKeylessPubFile (e) {
        e.preventDefault();
        this.LogoFile.delete('logo');
        this.LogoFile.append('logo', e.target.files[0]);
        this.LogoName = e.target.files[0].name;
      },
    },
    components: {
    }
  }
</script>
