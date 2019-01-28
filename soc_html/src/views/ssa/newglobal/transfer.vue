<template>
    <div class="pos-r" v-bind:style="{width: width, height:height}">
        <div v-show="status==0"
             class="textC"
             v-bind:style="{width: width, height:height,lineHeight:height}">
            <loading-normal :show.sync="true"></loading-normal>
        </div>
        <div v-show="status==1"
             class="textC ys-info-color"
             v-bind:style="{width: width, height:height,lineHeight:height}">
            <div class="d-i-b verticalM">
                <p style="line-height:1"><i class="ys-icon icon-chart-no-data"
                                            style="margin-left:6px;color:rgba(154,188,238,0.25);font-size: 60px;"></i>
                </p>
                <p style="line-height:1;color:rgba(154,188,238,0.7);" class="m-t-20">暂时没有数据</p>
            </div>
            <span style="display:none;">{{status}}</span>
        </div>
        <div v-show="status==2">
            <div v-bind:style="{width: width,height:height}">
                <div id="transfer-chart-{{ id }}"
                     v-bind:style="{width: width,height:height}"
                     v-on:resize="handleResize($event)">
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
</style>
<script>
    let echarts = require('echarts/lib/echarts');
    export default {
        name: "transfer-chart",
        props: {
            id: {
                default: 0
            },
            name: {
                default: ""
            },
            tipname: {
                default: "使用数"
            },
            width: {
                default: "100%"
            },
            height: {
                default: "200px"
            },
            color: {
                default: ""
            },
            data: {
                default: {}
            },
            unit: {
                default: ''
            },
        },
        data() {
            return {
                colors: ['#00BD85', '#4A92FF', '#D5B256', '#E96157', '#9abcee'],
            }
        },
        computed: {
            status: function () {
                this.setChart();
                return 2;
                // 0 加载之前   1 加载后无数据   2 加载后有数据
//                if (this.x === "") {
//                    return 0
//                } else {
//                    if (this.x.length > 0) {
//                        this.initChart();
//                        return 2
//                    } else {
//                        return 1
//                    }
//                }
            },
        },
        watch: {
            width() {
                if (this.data.pie_data) {
                    this.$nextTick(() => {
                        this.setChart();
                    })
                }
            },
            height() {
                if (this.data.pie_data) {
                    this.$nextTick(() => {
                        this.setChart();
                    })
                }
            },
            data() {
                this.setChart();
            }
        },
        methods: {
            initChart() {
                let self = this;
                let repeat = setInterval(function () {
                    if (document.getElementById('transfer-chart-' + self.id)) {
                        self.setChart();
                        window.addEventListener('resize', self.handleResize)
                        clearInterval(repeat)
                    }
                }, 300)
                let resizeRepeat = setInterval(function () {
                    if (document.getElementById('transfer-chart-' + self.id)) {
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
                        var resizeDiv = document.getElementById('transfer-chart-' + self.id);
                        EleResize.on(resizeDiv, function () {
                            self.handleResize();
                        });
                        clearInterval(resizeRepeat)
                    }
                }, 300)
            },
            setChart() {
                let self = this;
                if(self.chart) self.chart.dispose();
                if(!document.getElementById('transfer-chart-' + this.id)) return false;
                self.chart = echarts.init(document.getElementById('transfer-chart-' + this.id));
                let w = parseInt(this.width);
                let h = parseInt(this.height);
                let b = 'path://M12.36,10.13V39.87H9V10.13Z,M30.77,10.13Q41,10.13,41,18.88c0,5.87-3.46,8.83-10.29,8.83H22V39.87H18.6V10.13ZM22,24.75h8.54a8.23,8.23,0,0,0,5.33-1.46,5.47,5.47,0,0,0,1.71-4.41,5.09,5.09,0,0,0-1.75-4.33c-1.17-1-2.92-1.46-5.29-1.46H22Z';
                let a = 'path://M34.91,23.76H26.24V15.09a1.24,1.24,0,1,0-2.48,0V25A1.23,1.23,0,0,0,25,26.24h9.91a1.24,1.24,0,1,0,0-2.48ZM25,6.42A18.58,18.58,0,1,0,43.58,25,18.58,18.58,0,0,0,25,6.42ZM25,41.1A16.1,16.1,0,1,1,41.1,25,16.1,16.1,0,0,1,25,41.1Z';
                let c = 'path://M26.47,35.25v3.08h7.19v2.75H16.31V38.46h7.14l.16-3.08H4.48V8.92h41V35.25ZM42.76,11.73H7.27V32.28H42.76Z';
                let d = 'path://M405.333333 853.333333c23.466667 0 42.666667-19.2 42.666667-42.666667s-19.2-42.666667-42.666667-42.666667c-23.466667 0-42.666667 19.2-42.666667 42.666667S381.866667 853.333333 405.333333 853.333333zM840.533333 44.8c-10.666667-4.266667-21.333333 0-27.733333 8.533333C765.866667 128 701.866667 196.266667 584.533333 130.133333c-66.133333-36.266667-110.933333-25.6-140.8-6.4-32 19.2-53.333333 53.333333-59.733333 89.6C264.533333 224 170.666667 324.266667 170.666667 448l0 298.666667c0 130.133333 104.533333 234.666667 234.666667 234.666667s234.666667-104.533333 234.666667-234.666667L640 448c0-121.6-91.733333-221.866667-211.2-232.533333 4.266667-19.2 17.066667-40.533333 38.4-53.333333 29.866667-19.2 51.2-17.066667 98.133333 8.533333 81.066667 40.533333 132.266667 29.866667 174.933333 14.933333 49.066667-19.2 85.333333-59.733333 110.933333-108.8C855.466667 64 851.2 51.2 840.533333 44.8zM597.333333 746.666667c0 106.666667-85.333333 192-192 192s-192-85.333333-192-192L213.333333 512l384 0L597.333333 746.666667zM597.333333 448l0 21.333333L213.333333 469.333333l0-21.333333c0-98.133333 74.666667-179.2 170.666667-189.866667L384 469.333333l42.666667 0 0-211.2C522.666667 268.8 597.333333 349.866667 597.333333 448z';
                let img = [a, b, c, d];
                let arr = [], citys = [];

                for (let x = 0; x < 5; x++) {
                    arr[x] = [];
                    for (let y = 0; y < 4; y++) {
                        let obj = {
                            "name": '-',
                            "value": [(0.1 + y * 0.25) * w, (0.1 + x * 0.2) * h],
                            'symbol': img[y],
                            "symbolSize": '20',
                            "itemStyle": {"normal": {"color": self.colors[y]}},
                        };
                        citys.push(obj);
                        arr[x].push(obj);
                    }
                }
                /*------ start 初始化布局赋值 ------*/

                let data = self.data.pie_data;

                for (let i = 0; i < data.length; i++) {
                    arr[i][0]['name'] = data[i].time;
                    arr[i][1]['name'] = data[i].ip;
                    arr[i][2]['name'] = data[i].terminal;
                    arr[i][3]['name'] = data[i].operation;
                }
                /*------ end ------*/

                let data_line = [].concat(self.data.line_data), newLines = [];

                for (let i = 0; i < data_line.length; i++) {
                    let color = this.colors[i];
                    let obj = {
                        "fromName": data_line[i]['time'],
                        "toName": data_line[i]['ip'],
                        "coords": [],
                        lineStyle: {normal: {color: color, opacity: 0.5,}},
                    };
                    let obj_a = {
                        "fromName": data_line[i]['ip'],
                        "toName": data_line[i]['terminal'],
                        "coords": [],
                        lineStyle: {normal: {color: color, opacity: 0.5}},
                    };
                    let obj_b = {
                        "fromName": data_line[i]['terminal'],
                        "toName": data_line[i]['operation'],
                        "coords": [],
                        lineStyle: {normal: {color: color, opacity: 0.5}},
                    };
                    for (let x = 0; x < arr.length; x++) {
                        for (let y = 0; y < arr[x].length; y++) {
                            if (data_line[i]['time'] == arr[x][y]['name']) {
                                obj.coords.unshift(arr[x][y]['value'])
                            }
                            if (data_line[i]['ip'] == arr[x][y]['name']) {
                                obj.coords.push(arr[x][y]['value'])
                                obj_a.coords.unshift(arr[x][y]['value'])
                            }
                            if (data_line[i]['terminal'] == arr[x][y]['name']) {
                                obj_a.coords.push(arr[x][y]['value'])
                                obj_b.coords.unshift(arr[x][y]['value'])
                            }
                            if (data_line[i]['operation'] == arr[x][y]['name']) {
                                obj_b.coords.push(arr[x][y]['value'])
                            }
                        }
                    }
                    if(obj.coords.length > 2){obj.coords = obj.coords.slice(0,2)}
                    if(obj_a.coords.length > 2){obj_a.coords = obj_a.coords.slice(0,2)}
                    if(obj_b.coords.length > 2){obj_b.coords = obj_b.coords.slice(0,2)}
                    newLines.push(obj, obj_a, obj_b)
                };

                var allData = {
                    "citys": citys,
                    "newLines": newLines
                };
                self.option = {
                    geo: {
                        label: {
                            emphasis: {
                                show: false
                            }
                        },
                        roam: true,
                    },
                    series: [{
                        name: '地点',
                        type: 'effectScatter',
//                        type: 'scatter',
                        coordinateSystem: 'geo',
                        zlevel: 2,
                        rippleEffect: {
                            brushType: 'stroke',
                            period: 4,
                            scale: 2.5,
                            trailLength: 0,
                        },
                        label: {
                            normal: {
                                show: true,
                                position: [40, 5],
                                formatter: '{b}',
                            },
                            emphasis: {
                                show: true,
                                position: [40, 5],
                                formatter: '{b}'
                            }
                        },
                        symbolSize: 1,
                        showEffectOn: 'render',
                        itemStyle: {
                            normal: {
                                color: '#46bee9',
                            },
                        },
                        data: allData.citys
                    },
                        {
                            name: '线路',
                            type: 'lines',
                            coordinateSystem: 'geo',
                            zlevel: 1,
                            effect: {
                                show: true,
                                trailLength: 0.1,
                                symbolSize: 6,
                                period: 4,
                                symbol: 'triangle',
                            },
                            lineStyle: {
                                normal: {
                                    width: 0,
                                    curveness: 0.2,
                                    opacity: 1,
                                }
                            },
                            data: allData.newLines
                        },
                        {
                            name: '线路',
                            type: 'lines',
                            coordinateSystem: 'geo',
                            zlevel: 2,
                            effect: {
                                show: true,
                                period: 4,
                                symbol: 'triangle',//ECharts 提供的标记类型包括 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'
                                symbolSize: 6,
                                trailLength: 0,
                            },
                            lineStyle: {
                                normal: {
                                    color: this.colors[parseInt(Math.random() * 4)],
                                    width: 1,
                                    opacity: 0.4,
                                    curveness: 0.2
                                }
                            },
                            data: allData.newLines
                        }
                    ]
                };
                self.chart.setOption(self.option);
                window.addEventListener('resize', self.handleResize)
            },
            changeWanUnit(val) {
                if (val < 10000) {
                    return val + "条"
                } else {
                    val = (val / 10000).toFixed(2);
                    return val + "万条"
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
            handleResize() {
                this.chart.resize();
            },
        },
    }
</script>