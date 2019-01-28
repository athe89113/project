<template>
    <div class="" style="height:100%;width:100%">
        <div style="display:none">{{show}} -- {{shows}} </div>
        <div :id="id" :style="{width:'100%',height:box.height+'px',margin:'0 auto'}"
             v-if="(type!='number') && (type!='map') && (type!='scatter') && (type!='line-bar-chart') && (type!='loop') && (type!='funnel')"></div>
        <div :id="id" :style="{width:mapbox.width+'px',height:mapbox.height+'px',margin:'0 auto'}"
             v-if="type=='map'"></div>
        <div :style="{width:box.width+'px',height:box.height+'px',margin:'0 auto'}" v-if="type=='number'">
            <div style="padding-top:40px;">
                <p class="ys-info-color textC">{{name}}</p>
                <p class="textC"><span class="font36 m-r-5">{{total}}</span>个</p>
            </div>
        </div>
        <div class="ys-box" :style="{height:box.height+'px',paddingTop:'10px',margin:'auto'}" v-if="type=='table'">
            <div id="attack-event-24-hour-box">
                <table class="ys-chart-table">
                    <thead>
                    <tr>
                        <th v-for="item in listThead" track-by="$index">{{item}}</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(i,item) in listTbody">
                        <td v-for="(j,hitem) in listThead">{{listTbody[i][j]}}</td>
                    </tr>
                    </tbody>
                </table>
                <no-data :height="'219px'" v-if="attackEvent24HourData.length==0"></no-data>
            </div>
        </div>
        <!-- 散点图 -->
        <scatter-chart v-if="type=='scatter'"
                       :height="box.height"
                       :datas="datas"></scatter-chart>
        <!-- 环形图 -->
        <loop-chart v-if="type=='loop'"
                    :height="box.height"
                    :datas="datas"
                    :name="name"></loop-chart>
        <!-- 漏斗图 -->
        <funnel-chart v-if="type=='funnel'"
                      :height="box.height"
                      :datas="datas"
                      :name="name"></funnel-chart>
        <!-- 单数据 条形图-->
        <ling-bar-chart v-if="type=='line-bar-chart'"
                        :height="box.height"
                        :datas="datas"
                        :name="'异常事件'"
                        :color="'#dabb61'"
                        :unit="'次'"></ling-bar-chart>
    </div>
</template>
<style scoped>
    .ys-chart-table tr th {
        text-align: center;
        color: #93a6d8;
        padding-bottom: 8px;
    }

    .ys-chart-table td {

    }
</style>
<script>
    let echarts = require('echarts/lib/echarts');
    let collect = require('collect.js')
    let provinces = require("better-echarts-maps/dist/china-provinces.js")
    let cityCoordinate = require("better-echarts-maps/dist/china-cities-coordinate.js")
    // 新增
    import scatterChart from '../../../components/chart/scatter-chart'
    import lingBarChart from '../../../components/chart/ling-bar-chart'
    import loopChart from '../../../components/chart/loop'
    import funnelChart from '../../../components/chart/funnel'

    var _ = require('lodash');
    export default {
        name: "template-chart",
        components: {
            scatterChart,
            lingBarChart,
            loopChart,
            funnelChart
        },
        props: {
            type: {
                default: "line"
            },
            info: {
                type: Object,
                default() {
                    return {
                        data: [],
                        labels: []
                    }
                }
            },
            datas: {
                type: Object,
                dafault: function () {
                    return {
                        x: {},
                        y: {}
                    }
                }
            },
            tablechart: {
                x: {},
                y: {}
            }, // table 数据
            mapchart: {
                type: Object,
                default() {
                    return {
                        pinyin: '',
                    }
                }
            }, // 地图
            name: "",
            show: {
                type: Boolean,
                default: false
            },
            unit: null,
            mapbox: {
                type: Object,
                default() {
                    return {
                        width: "100%",
                        height: 200,
                        xName: '',
                        yName: ''
                    }
                }
            },
            box: {
                type: Object,
                default() {
                    return {
                        width: 400,
                        height: 200,
                        xName: '',
                        yName: ''
                    }
                }
            },
            mapdata: {
                type: Object,
                default() {
                    return {
                        list: [],
                        map_text: '',
                        pinyin: ''
                    }
                }
            },
        },
        data() {
            return {
                barColor: ['#4993fd', '#3a9be5', '#27a6c6', '#12b2a3', '#03bb89'],
                prevId: "",
                shows: false,
                listThead: [],
                listTbody: [],
                attackEvent24HourData: [],
                id: '',
                chart: null,
                newData: {},
                newDataUp: false
            }
        },
        computed: {
            total: function () {
                let num = 0;
                for (let x in this.info.data) {
                    num += collect(this.info.data[x].data).sum()
                }
                return num;
            },
        },
        ready() {
            this.changeStatus();
            this.debouncedGetAnswer = _.debounce(function (val) {
                this.changeStatus()
            }, 2000)
        },
        methods: {
            getRandomId() {
                var str = "";
                for (var i = 0; i < 6; i++) {
                    var num = Math.random() * 9;
                    num = parseInt(num, 10);
                    str += num;
                }
                this.id = this.type + "-template-chart-" + str;
                let repeat = setInterval(function () {
                    if (document.getElementById(self.id)) {
                        window.addEventListener('resize', self.handleResize)
                        var EleResize = {
                            _handleResize: function (e) {
                                var ele = e.target || e.srcElement;
                                var trigger = ele.__resizeTrigger__;
                                if (trigger) {
                                    var handlers = trigger.__z_resizeListeners;
                                    if (handlers) {
                                        var size = handlers.length;
                                        for (var i = 0; i < size; i++) {
                                            var h = handlers[i];
                                            var handler = h.handler;
                                            var context = h.context;
                                            handler.apply(context, [e]);
                                        }
                                    }
                                }
                            },
                            _removeHandler: function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    var size = handlers.length;
                                    for (var i = 0; i < size; i++) {
                                        var h = handlers[i];
                                        if (h.handler === handler && h.context === context) {
                                            handlers.splice(i, 1);
                                            return;
                                        }
                                    }
                                }
                            },
                            _createResizeTrigger: function (ele) {
                                var obj = document.createElement('object');
                                obj.setAttribute('style',
                                    'display: block; position: absolute; top: 0; left: 0; height: 100%; width: 100%; overflow: hidden;opacity: 0; pointer-events: none; z-index: -1;');
                                obj.onload = EleResize._handleObjectLoad;
                                obj.type = 'text/html';
                                ele.appendChild(obj);
                                obj.data = 'about:blank';
                                return obj;
                            },
                            _handleObjectLoad: function (evt) {
                                this.contentDocument.defaultView.__resizeTrigger__ = this.__resizeElement__;
                                this.contentDocument.defaultView.addEventListener('resize', EleResize._handleResize);
                            }
                        };
                        if (document.attachEvent) {//ie9-10
                            EleResize.on = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (!handlers) {
                                    handlers = [];
                                    ele.__z_resizeListeners = handlers;
                                    ele.__resizeTrigger__ = ele;
                                    ele.attachEvent('onresize', EleResize._handleResize);
                                }
                                handlers.push({
                                    handler: handler,
                                    context: context
                                });
                            };
                            EleResize.off = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    EleResize._removeHandler(ele, handler, context);
                                    if (handlers.length === 0) {
                                        ele.detachEvent('onresize', EleResize._handleResize);
                                        delete  ele.__z_resizeListeners;
                                    }
                                }
                            }
                        } else {
                            EleResize.on = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (!handlers) {
                                    handlers = [];
                                    ele.__z_resizeListeners = handlers;

                                    if (getComputedStyle(ele, null).position === 'static') {
                                        ele.style.position = 'relative';
                                    }
                                    var obj = EleResize._createResizeTrigger(ele);
                                    ele.__resizeTrigger__ = obj;
                                    obj.__resizeElement__ = ele;
                                }
                                handlers.push({
                                    handler: handler,
                                    context: context
                                });
                            };
                            EleResize.off = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    EleResize._removeHandler(ele, handler, context);
                                    if (handlers.length === 0) {
                                        var trigger = ele.__resizeTrigger__;
                                        if (trigger) {
                                            trigger.contentDocument.defaultView.removeEventListener('resize', EleResize._handleResize);
                                            ele.removeChild(trigger);
                                            delete ele.__resizeTrigger__;
                                        }
                                        delete  ele.__z_resizeListeners;
                                    }
                                }
                            }
                        }
                        var resizeDiv = document.getElementById(self.id);
                        EleResize.on(resizeDiv, function () {
                            self.handleResize()
                        });
                        clearInterval(repeat)
                    }
                }, 300)
                this.$nextTick(() => {
                    this.setChart()
                })
            },
            handleResize() {
                this.chart.resize();
            },
            setChart() {
                if (this.chart) this.chart.dispose();
                if (this.type == "line") {
                    this.setLineChart()
                } else if (this.type == "pie") {
                    this.setPieChart()
                } else if (this.type == "bar_x") {
                    this.setBarXChart()
                } else if (this.type == "bar_y") {
                    this.setBarYChart()
                } else if (this.type == "number") {
                    this.setNumberChart()
                } else if (this.type == "table") {
                    this.setTableChart()
                } else if (this.type == "map") {
                    this.setMapChart()
                } else if (this.type == "scatter") {
                    this.newData = this.datas
                    this.newDataUp = true;
                } else if (this.type == "loop") {
                    this.newData = this.datas
                    this.newDataUp = true;
                } else if (this.type == "funnel") {
                    this.newData = this.datas
                    this.newDataUp = true;
                }
            },
            changeUnit(val) {
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
            changeNumber(val, bl) {
                let num = val;
                if (bl) {
                    if (num > Math.pow(10, 12)) {
                        num = (num / Math.pow(10, 12)).toFixed(2) + "兆"
                    } else if (num > Math.pow(10, 8)) {
                        num = (num / Math.pow(10, 8)).toFixed(2) + "亿"
                    } else if (num > Math.pow(10, 4)) {
                        num = (num / Math.pow(10, 4)).toFixed(2) + "万"
                    }
                } else {
                    if (num > Math.pow(10, 12)) {
                        num = (num / Math.pow(10, 12)).toFixed(0) + "兆"
                    } else if (num > Math.pow(10, 8)) {
                        num = (num / Math.pow(10, 8)).toFixed(0) + "亿"
                    } else if (num > Math.pow(10, 4)) {
                        num = (num / Math.pow(10, 4)).toFixed(0) + "万"
                    }
                }

                return num
            },
            setLineChart() {
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let Xname = [];
                let xData = [];
                for (let x in curInfo.data) {
                    curSeries.push({
                        data: curInfo.data[x].data,
                        type: 'line',
                        name: curInfo.data[x].name
                    })
                    Xname.push(curInfo.data[x].name)
                }
                for (let x in curInfo.labels) {
                    xData.push(curInfo.labels[x])
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    toolbox: {
                        show: true,
                        feature: {
                            // mark : {show: true},
                            // dataZoom: {
                            //   yAxisIndex: 'none'
                            // },
                            // restore : {show: true},
                            // saveAsImage : {
                            //     show: true,
                            //     pixelRatio: 1,
                            //     title : '下载',
                            //     type : 'png',
                            //     lang : ['点击保存'],
                            //     iconStyle:{
                            //       borderColor: "#5ca9e5",
                            //     }
                            // }
                        }
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: "#dfdfe7",
                                opacity: 0.2
                            },
                        },
                        formatter: function (params) {
                            let str = params[0].name
                            for (var i = 0; i < params.length; i++) {
                                if (self.unit == "band") {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                                } else if (self.unit == "number") {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeNumber(params[i].value, 1)
                                } else {
                                    str += "<br/>" + params[i].seriesName + ":" + params[i].value
                                }
                            }
                            return str
                        }
                    },
                    grid: {
                        top: '25',
                        bottom: '15',
                        left: 10,
                        right: '5%',
                        containLabel: true
                    },
                    calculable: true,
                    color: [
                        'rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)',
                        'rgba(74,126,155,0.8)', 'rgba(24,146,55,0.8)', 'rgba(14,46,75,0.8)', 'rgba(174,16,55,0.8)',
                        'rgba(126,74,155,0.8)', 'rgba(146,24,55,0.8)', 'rgba(46,14,75,0.8)', 'rgba(16,174,55,0.8)',
                    ],
                    xAxis: {
                        name: this.box.xName,
                        nameTextStyle: {
                            color: "#fff"
                        },
                        type: 'category',
                        data: xData,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        axisLabel: {
                            rotate: -30,
                            textStyle: {color: "#dfdfe7"}
                        }
                    },
                    yAxis: {
                        name: this.box.yName,
                        nameTextStyle: {
                            color: "#fff"
                        },
                        type: 'value',
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        splitNumber: 5,
                        axisLabel: {
                            textStyle: {color: "#dfdfe7"},
                            padding: [3, 3, 3, 3],
                            formatter: function (value, index) {
                                if (self.unit == "band") {
                                    return self.changeUnit(value)
                                } else if (self.unit == "number") {
                                    return self.changeNumber(value)
                                } else {
                                    return value
                                }
                            }
                        },//y轴坐标的字颜色
                        splitLine: {
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        }
                    },
                    legend: {
                        data: Xname,
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    series: curSeries
                };
                this.chart.setOption(option);
                // console.log(chart.getDataURL({ pixelRatio: 2}))
            },
            setPieChart() {
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let legentData = [];
                for (let x in curInfo.data) {
                    let sum = 0;
                    curInfo.data[x].data.forEach(function (val) {
                        sum += val
                    })
                    curSeries.push({
                        name: curInfo.data[x].name,
                        value: sum,
                    });
                    legentData.push(curInfo.data[x].name)
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    color: [
                        '#00bd85', '#e96157', '#dabb61', '#4a92ff', '#0ffd85',
                        '#ecc157', '#deeb61', '#41934f', '#4acc12', '#f0f85d',
                        '#272727', '#4D0000', '#820041', '#5E005E', '#3A006F',
                        '#3C3C3C', '#600000', '#9F0050', '#750075', '#4B0091',
                        '#4F4F4F', '#750000', '#BF0060', '#930093', '#5B00AE',
                        '#5B5B5B', '#930000', '#D9006C', '#AE00AE', '#6F00D2',],
                    grid: {
                        top: '15%',
                        bottom: '30',
                        // left:10,
                        right: '15%',
                        containLabel: true
                    },
                    legend: {
                        show: true,
                        bottom: 5,
                        x: 'center',
                        y: 'bottom',
                        data: legentData,
                        textStyle: {
                            color: "#f2f2f2"
                        },
                        itemWidth: 10,
                        itemHeight: 10,
                        itemGap: 5
                    },
                    series: [
                        {
                            name: "",
                            type: 'pie',
                            radius: ['23%', '67%'],
                            center: ['50%', '40%'],
                            data: curSeries,
                            itemStyle: {
                                normal: {
                                    opacity: 0.8
                                }
                            },
                            label: {
                                normal: {
                                    show: false
                                }
                            }
                        }
                    ]
                };
                this.chart.setOption(option);
            },
            setNumberChart() {
            },
            setTableChart() {
                let TableData = this.tablechart;
                let arr = [], data = [];
                if (this.tablechart == undefined) {
                    return false
                }
                this.listThead = [];
                let objs = {};
                objs = Object.assign({}, TableData.x, TableData.y);
                for (let key in objs) {
                    this.listThead.push(key)
                }
                for (let key in objs) {
                    data.push(objs[key]);
                }
                if (data.length != 0) {
                    for (var i = 0; i < data[0].length; i++) {
                        let temp = [];
                        for (let y = 0; y < data.length; y++) {
                            temp.push(data[y][i])
                        }
                        arr.push(temp)
                    }
                }

                // console.log(arr)

                // for(let key in TableData.x){
                //   this.listThead.push(key)
                //   for(let i in TableData.x[key]){
                //     arr.push([TableData.x[key][i]])
                //   }
                // }
                // for(let key in TableData.y){
                //   this.listThead.push(key)
                //   for(let i in TableData.y[key]){
                //     arr[i].push(TableData.y[key][i])
                //   }
                // }
                this.listTbody = [].concat(arr)
            },
            setMapChart() {
                //console.log(provinces.ChinaProvinces);
                //console.log(cityCoordinate);

                let data = this.mapdata.list;
                let text = this.mapdata.map_text;

                var curMap;

                if (this.mapdata.pinyin != undefined && this.mapdata.pinyin != "") {
                    curMap = this.mapdata.pinyin
                } else {
                    curMap = this.mapchart.pinyin;
                }
                var convertData = function (data) {
                    var res = [];
                    for (var i = 0; i < data.length; i++) {
                        var geoCoord = geoCoordMap[data[i].name];
                        if (geoCoord) {
                            res.push({
                                name: data[i].name,
                                value: geoCoord.concat(data[i].value)
                            });
                        }
                    }
                    return res;
                };


                let curMapData = {};
                for (let x in provinces.ChinaProvinces) {
                    if (provinces.ChinaProvinces[x][0] == curMap) {
                        curMapData = provinces.ChinaProvinces[x][1]
                    }
                }
                echarts.registerMap(curMap, curMapData);
                this.chart = echarts.init(document.getElementById(this.id));
                var geoCoordMap = cityCoordinate.ChinaCitiesCoordinate;
                var option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: function (params) {
                            let data = params.data
                            //console.log(params)
                            return data.name + "<br/>" + text + ":" + data.value[2]
                        }
                    },
                    geo: {
                        map: curMap,
                        zoom: 1.2,
                        label: {
                            emphasis: {
                                show: true,
                                formatter: function (params) {
                                    return params.name
                                },
                                color: "#f2f2f2"
                            }
                        },
                        roam: false,
                        itemStyle: {
                            normal: {
                                borderColor: 'rgba(74,146,255,0.6)',
                                borderWidth: 0.5,
                                areaColor: 'rgba(0,0,0,0.15)',
                            },
                            emphasis: {
                                areaColor: 'rgba(74,146,255,0.3)'
                            }
                        },
                    },
                    series: [{
                        name: "",
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        zlevel: 3,
                        rippleEffect: {
                            brushType: 'stroke',
                            period: 2,
                            scale: 15
                        },
                        itemStyle: {
                            normal: {
                                color: "#4a92ff"
                            }
                        },
                        symbolSize: 5,
                        data: convertData(data)
                    }]
                };
                this.chart.setOption(option);
            },
            setBarXChart() {
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let Xname = [];
                let xData = [];
                let xType = 'value', maxArr = [];
                for (let x in curInfo.data) {
                    curSeries.push({
                        name: curInfo.data[x].name,
                        type: 'bar',
                        data: curInfo.data[x].data,
                        barMaxWidth: 20,
                    })
                    maxArr = curInfo.data[x].data
                    Xname.push(curInfo.data[x].name)
                }
                var max = Math.max.apply(null, maxArr);
                if (max > Math.pow(10, 8)) {
                    xType = 'log'
                }
                for (let x in curInfo.labels) {
                    xData.push(curInfo.labels[x])
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                        formatter: function (params) {
                            let str = params[0].name
                            for (var i = 0; i < params.length; i++) {
                                if (self.unit == "band") {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                                } else if (self.unit == "number") {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeNumber(params[i].value, 1)
                                } else {
                                    str += "<br/>" + params[i].seriesName + ":" + params[i].value
                                }
                            }
                            return str
                        }
                    },
                    grid: {
                        top: '20',
                        bottom: '30',
                        left: 10,
                        right: '5%',
                        containLabel: true
                    },
                    calculable: true,
                    color: [
                        'rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)',
                        'rgba(74,126,155,0.8)', 'rgba(24,146,55,0.8)', 'rgba(14,46,75,0.8)', 'rgba(174,16,55,0.8)',
                        'rgba(126,74,155,0.8)', 'rgba(146,24,55,0.8)', 'rgba(46,14,75,0.8)', 'rgba(16,174,55,0.8)',
                    ],
                    xAxis: [
                        {
                            name: '',
                            type: 'category',
                            data: xData,
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: "0.75"
                                }
                            },
                            axisTick: {
                                show: false,
                            },
                            axisLabel: {
                                textStyle: {color: "#93a6d8"},
                                formatter: function (value, index) {
                                    let str = value;
                                    if (value.length > 8) {
                                        str = value.substring(0, 8) + '...'
                                    }
                                    return str
                                },
                            },//x轴坐标的字颜色
                        }
                    ],
                    yAxis: [
                        {
                            name: '',
                            type: xType,
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: "0.75"
                                }
                            },
                            axisTick: {
                                show: false,
                            },
                            splitNumber: 5,
                            axisLabel: {
                                textStyle: {color: "#93a6d8"},
                                formatter: function (value, index) {
                                    if (self.unit == "band") {
                                        return self.changeUnit(value)
                                    } else if (self.unit == "number") {
                                        return self.changeNumber(value)
                                    } else {
                                        return value
                                    }
                                }
                            },//y轴坐标的字颜色
                            splitLine: {
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: "0.75"
                                }
                            }
                        }
                    ],
                    legend: {
                        data: Xname,
                        textStyle: {
                            color: '#93a6d8'
                        }
                    },
                    series: curSeries
                };
                this.chart.setOption(option);
            },
            setBarYChart() {
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let Xname = [];
                let yData = [];
                let xType = 'value', maxArr = [];
                for (let x in curInfo.data) {
                    curSeries.push({
                        name: curInfo.data[x].name,
                        type: 'bar',
                        barMaxWidth:20,
                        data: curInfo.data[x].data,
                    })
                    maxArr = curInfo.data[x].data;
                    Xname.push(curInfo.data[x].name)
                }
                var max = Math.max.apply(null, maxArr);
                if (max > Math.pow(10, 8)) {
                    xType = 'log'
                }
                for (let x in curInfo.labels) {
                    yData.push(curInfo.labels[x])
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        },
                        formatter: function (params) {
                            let str = params[0].name
                            for (var i = 0; i < params.length; i++) {
                                if (self.unit == "band") {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                                } else if (self.unit == "number") {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeNumber(params[i].value, 1)
                                } else {
                                    str += "<br/>" + params[i].seriesName + ":" + params[i].value
                                }
                            }
                            return str
                        }
                    },
                    grid: {
                        top: '20',
                        bottom: '30',
                        left: 10,
                        right: '5%',
                        containLabel: true
                    },
                    color: [
                        'rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)',
                        'rgba(74,126,155,0.8)', 'rgba(24,146,55,0.8)', 'rgba(14,46,75,0.8)', 'rgba(174,16,55,0.8)',
                        'rgba(126,74,155,0.8)', 'rgba(146,24,55,0.8)', 'rgba(46,14,75,0.8)', 'rgba(16,174,55,0.8)',
                    ],
                    xAxis: {
                        name: '',
                        type: xType,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        splitNumber: 5,
                        splitLine: {
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisLabel: {
                            textStyle: {color: "#93a6d8"},
                            formatter: function (value, index) {
                                if (self.unit == "band") {
                                    return self.changeUnit(value)
                                } else if (self.unit == "number") {
                                    return self.changeNumber(value)
                                } else {
                                    return value
                                }
                            }
                        },//x轴坐标的字颜色
                    },
                    yAxis: {
                        name: '',
                        type: 'category',
                        data: yData,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        axisLabel: {
                            textStyle: {color: "#93a6d8"},

                        },//x轴坐标的字颜色
                    },
                    legend: {
                        data: Xname,
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    series: curSeries
                };
                this.chart.setOption(option);
            },
            changeStatus() {
                // 0 加载之前   1 加载后无数据   2 加载后有数据
                this.status = 0;
                setTimeout(() => {
                    if (this.datas == undefined || JSON.stringify(this.datas) == '{}') {
                        this.status = 1;
                    } else if (this.info && this.info.labels.length) {
                        this.getRandomId();
                        this.status = 2;
                    } else {
                        if (this.datas.x === "") {
                            this.status = 1;
                        } else {
                            for (let key in this.datas.x) {
                                if (this.datas.x[key].length > 0) {
                                    this.getRandomId();
                                    this.status = 2;
                                } else {
                                    this.status = 1;
                                }
                            }
                        }
                    }
                }, 1000)
            },
        },
        watch: {
            'mapchart': function (val) {
                this.setMapChart()
            },
            'show': function (val) {
                if (this.chart) this.chart.dispose();
                this.debouncedGetAnswer()
            }
        }
    }
</script>