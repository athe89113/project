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
                <div id="bubble-chart-{{ id }}"
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
        name: "bubble-chart",
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
                 //0 加载之前   1 加载后无数据   2 加载后有数据
                if (this.data === "") {
                    return 0
                } else {
                    if (this.data.length > 0) {
                        this.initChart();
                        return 2
                    } else {
                        return 1
                    }
                }
            },
        },
        methods: {
            initChart() {
                let self = this;
                let repeat = setInterval(function () {
                    if (document.getElementById('bubble-chart-' + self.id)) {
                        self.setChart();
                        window.addEventListener('resize', self.handleResize)
                        clearInterval(repeat)
                    }
                }, 300)
                let resizeRepeat = setInterval(function () {
                    if (document.getElementById('bubble-chart-' + self.id)) {
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
                        var resizeDiv = document.getElementById('bubble-chart-' + self.id);
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
                if(!document.getElementById('bubble-chart-' + this.id)) return false;

                let colors = ['#F05D5F', '#4A92FF', '#53ADF8'];
                var plantCap = this.data;
                var datalist = [[56, 68], [35, 90], [20, 63], [83, 20], [36, 30], [64, 10], [75, 75], [93, 72], [0, 12], [50, 6], [100, 20], [10, 20], [20, 0], [0, 100], [20, 120], [50, 120],[70,120],[90,120],[100,120]];
                let datas = [];
                for (var i = 0; i < plantCap.length; i++) {
                    var item = plantCap[i];
                    var itemToStyle = datalist[i];
                    datas.push({
                        name: item.name + '\n\n' + self.changeWanUnit(item.value),
                        value: itemToStyle,
                        symbolSize: 100 - i * 3,
                        label: {
                            normal: {
                                textStyle: {
                                    fontSize: 11
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: colors[i<5?0:i>10?2:1],
                                opacity: (Math.random() * 4 + 6) / 10
                            }
                        },
                    })
                }
                self.chart = echarts.init(document.getElementById('bubble-chart-' + this.id));
                let statusOption = {
                    grid: {
                        show: false,
                    },
                    xAxis: [{
                        gridIndex: 0,
                        type: 'value',
                        show: false,
                        min: 0,
                        max: 100,
                        nameLocation: 'middle',
                        nameGap: 5
                    }],
                    yAxis: [{
                        gridIndex: 0,
                        min: 0,
                        show: false,
                        max: 100,
                        nameLocation: 'middle',
                        nameGap: 30
                    }],
                    series: [{
                        type: 'scatter',
                        symbol: 'circle',
                        symbolSize: 100,
                        label: {
                            normal: {
                                show: true,
                                formatter: '{b}',
                                color: '#fff',
                                textStyle: {
                                    fontSize: '20'
                                }
                            },
                        },
                        itemStyle: {
                            normal: {
                                color: '#00acea'
                            }
                        },
                        data: datas
                    }]
                };
                self.chart.setOption(statusOption);
                window.addEventListener('resize', self.handleResize)
            },
            changeWanUnit(val) {
                if (val < 10000) {
                    return val
                } else if (val >= 10000 && val < 10000 * 10000) {
                    val = (val / 10000).toFixed(2);
                    return val + "万"
                } else {
                    val = (val / (10000 * 10000)).toFixed(2);
                    return val + "亿"
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