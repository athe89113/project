<template>
    <div class="ys-box">
        <div class="ys-box-con ys-wrap">
            <div class="tool-box">
                <div class="fRight d-i-b">
                    <div>
                        <button class="ys-btn" @click="showAdd()"><i class="ys-icon icon-add-circle"></i>添加SM词</button>
                    </div>
                </div>
                <div class="fLeft d-i-b">
                    <div class="ys-search d-i-b m-l-10">
                        <input type="text" placeholder="输入关键词查询"
                               v-model="searchValue"
                               @keyup.enter="tableRe()"
                               class="ys-input" style="width:180px;"/>
                        <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
                    </div>
                </div>
            </div>
            <table class="ys-table m-t-10">
                <thead>
                <tr>
                    <th>SM词</th>
                    <th>操作</th>
                </tr>
                </thead>
                <tbody>
                <template v-for="list in tableList">
                    <tr v-bind:class="[$index%2==1 ? 'even' : 'odd', showId==list.id? 'shown': ''] ">
                        <td>{{ list.word }}</td>
                        <td class="operate">
                            <tooltip :content="'编辑'" :delay="1000">
                                <a @click="showEdit(list)"><i class="ys-icon icon-edit"></i></a>
                            </tooltip>
                            <ys-poptip confirm
                                       title="您确认删除此SM词吗？"
                                       :placement="'left'"
                                       @on-ok="del(list.id)"
                                       @on-cancel="">
                                <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
                            </ys-poptip>
                        </td>
                    </tr>
                </template>
                </tbody>
            </table>
            <ys-table :url="tableUrl" :data.sync="tableList" :filter.sync="tableFilter" :search.sync="searchValue"
                      v-ref:table></ys-table>
        </div>
        <aside :show.sync="configStatus"
               :header="configHead"
               :left="'auto'"
               :width="'500px'">
            <div>
                <validator name="valCompany" @valid="onValid = true" @invalid="onValid = false">
                    <div v-if="!showQRCode">
                        <div class="ys-box-title ys-box-title-s">
                            <i class="ys-icon icon-title ys-primary-color m-r-5"></i>
                            <span>设置同时包含时，多个词之间使用英文分号隔开，如“网盾;5.1.0”</span>
                        </div>
                        <table class="ys-form-table m-t-10">
                            <tbody>
                            <tr>
                                <td style="width: 60px">SM词:</td>
                                <td>
                                    <input class="ys-input"
                                           v-model="sm.word"
                                           placeholder="最多50个字符"
                                           style="width: 218px"
                                           v-validate:word="['required']">
                                </td>
                            </tr>
                            </tbody>

                        </table>
                        <div class="aside-foot m-t-20">
                            <button class="ys-btn m-r-10" @click="changeConfig()">确定</button>
                            <button class="ys-btn ys-btn-white" @click="configStatus=false">取消</button>
                        </div>
                    </div>
                </validator>
            </div>

        </aside>
    </div>
</template>
<script>
    import Api from '../../../lib/api'
    import ysTable from 'src/components/table-data.vue'
    import ysSelect from 'src/components/select.vue'
    import ysPoptip from 'src/components/poptip.vue'
    import aside from 'src/components/Aside.vue'

    export default {
        name: "sm-mgt",
        props: [],
        computed: {},
        data() {
            return {
                showAddUser: false,
                userIsAdmin: localStorage.getItem('is_admin'),
                tableUrl: '/api/op_store/sm/dts',
                tableList: "",
                tableFilter: {
                    company_id: {id: this.companyId, name: ""},
                },
                searchValue: "",
                showQRCode: false,
                //添加
                configStatus: false,
                configHead: "",
                editType: 0,
                editId: "",
                delId: "",
                sm: {
                    id: 0,
                    word: "",
                },
            }
        },
        ready: function () {
        },
        methods: {
            tableRe() {
                var self = this;
                self.$refs.table.Re();
            },
            showAdd() {
                this.configStatus = true;
                this.editId = 0;
                this.showQRCode = false;
                this.editType = 0;
                this.sm = {
                    id: 0,
                    word: ""
                }
                this.configHead = '添加'
            },
            showEdit(list) {
                this.configStatus = true;
                this.editId = list.id;
                this.getSmInfo();
                this.showQRCode = false;
                this.editType = 1;
                this.configHead = '编辑'
            },
            getSmInfo() {
                let self = this;
                self.$http.get('/api/op_store/sm/' + self.editId).then(function (response) {
                    if (response.data.status == 200) {
                        self.sm = response.data.data
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            del(id) {
                this.delId = id;
                this.$http.delete('/api/op_store/sm/' + this.delId).then(function (response) {
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                    this.tableRe();
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            changeConfig() {
                if (this.editType == 0) {
                    this.$http.post('/api/op_store/sm', this.sm).then(function (response) {
                        if (response.data.status == 200) {
                            this.$root.alertSuccess = true;
                            this.showQRCode = false;
                            this.configStatus = false;
                            this.tableRe();
                        } else {
                            this.$root.alertError = true;
                        }
                        this.$root.errorMsg = response.data.msg;
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                } else {
                    this.$http.put('/api/op_store/sm', this.sm).then(function (response) {
                        this.$root.errorMsg = response.data.msg;
                        if (response.data.status == 200) {
                            this.$root.alertSuccess = true;
                            this.showQRCode = false;
                            this.configStatus = false;
                            this.tableRe();
                        } else {
                            this.$root.alertError = true;
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                }
            }
        },
        components: {
            ysTable,
            ysSelect,
            ysPoptip,
            aside,
        }
    }

</script>