<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="col-md-12 col-lg-6 m-t-10">
        <div class="ys-card-box">
              <p>cpu使用率(60分钟)</p>
              <line-chart
                      :id="'mon-cpu'"
                      :height="'240px'"
                      :name="cpu.name"
                      :x="cpu.x"
                      :color="cpu.color"
                      :series="cpu.series"
                      :unit="'percent'"
              ></line-chart>
            </div>

      </div>
      <div class="col-md-12 col-lg-6 m-t-10">
        <div class="ys-card-box">
              <p>网卡流量(60分钟)</p>
              <line-chart
                      :id="'mon-nets'"
                      :height="'240px'"
                      :name="nets.name"
                      :x="nets.x"
                      :color="nets.color"
                      :series="nets.series"
                      :unit="'band'"
              ></line-chart>
            </div>
      </div>
      <div class="col-md-12 col-lg-6 m-t-10">
        <div class="ys-card-box">
              <p>内存使用率(60分钟)</p>
              <line-chart
                      :id="'mon-mem'"
                      :height="'240px'"
                      :name="mem.name"
                      :x="mem.x"
                      :color="mem.color"
                      :series="mem.series"
                      :unit="'percent'"
              ></line-chart>
            </div>
      </div>
      <div class="col-md-12 col-lg-6 m-t-10">
        <table class="ys-table">
          <thead>
          <tr>
            <th>磁盘</th>
            <th>总量</th>
            <th>已使用</th>
            <th>剩余容量</th>
            <th>剩余百分比</th>
          </tr>
          </thead>
          <tbody>
          <tr class="odd" v-for="disk in disks">
            <td>{{disk.name}}</td>
            <td>{{disk.all | changeUnit}}</td>
            <td>{{disk.used | changeUnit}}</td>
            <td>{{disk.all - disk.used | changeUnit}}</td>
            <td>{{100 - (disk.used / disk.all *100) | toPrecision}}%</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import Api from 'src/lib/api'
  export default {
    name: 'system-resource',
    data () {
      return {
        cpu: {
          name: ["使用率"],
          x: [],
          color: ['#dabb61'],
          series: [
            {data: []},
          ]
        },
        mem: {
          name: ["使用率"],
          x: [],
          color: ['#4a92ff'],
          series: [
            {data: []},
          ]
        },
        nets: {
          name: ["入口流量", "出口流量"],
          x: [],
          color: ['#00bd85','#4a92ff'],
          series: [
            {data: []},
            {data: []},
          ]
        },
        disks: [
          {"name": "/", "used": 30, "all": 100, "free": 70},
          {"name": "/opt", "used": 30, "all": 100, "free": 70},
        ],
      }
    },
    ready: function () {
      this.fetchCpu()
      this.fetchMem()
      this.fetchNets()
      this.fetchDisk()
    },
    filters: {
      changeUnit(val){
        if (val < 1024) {
          return val + "b"
        } else if (val >= 1024 && val < 1024 * 1024) {
          val = (val / 1024).toFixed(1);
          return val + "Kb"
        } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024)).toFixed(1);
          return val + "Mb"
        } else if (val >= 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024 * 1024)).toFixed(1);
          return val + "Gb"
        }
      },
      toPrecision(val){
        return val.toPrecision(2)
      }
    },
    methods: {
      fetchCpu(){
        this.$http.get('/api/system/monitor?item=cpu').then( (response) => {
          let data = response.data.data
          if (response.data.status == 200) {
            this.cpu.x = data.time
            this.cpu.series[0].data = data.data
          }
          else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      fetchMem(){
        this.$http.get('/api/system/monitor?item=mem').then( (response) => {
          let data = response.data.data
          if (response.data.status == 200) {
            this.mem.x = data.time
            this.mem.series[0].data = data.data
          }
          else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      fetchNets(){
        this.$http.get('/api/system/monitor?item=net').then( (response) => {
          let data = response.data.data
          let inNet = []
          let outNet = []
          if (response.data.status == 200) {
            this.nets.x = data.time
            data.data.forEach((item) => {
              inNet.push(item['in'])
              outNet.push(item['out'])
            })
            this.nets.series[0].data = inNet
            this.nets.series[1].data = outNet
          }
          else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      fetchDisk(){
        this.$http.get('/api/system/monitor?item=disk').then( (response) => {
          let data = response.data.data
          if (response.data.status == 200) {
            this.disks = data["data"][data["data"].length -1]
          }
          else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
    },
    components: {}

  }
</script>