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
                <div id="coordinate-chart-{{ id }}"
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
        name: "coordinate-chart",
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
                    if (this.data.data.length > 0) {
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
                    if (document.getElementById('coordinate-chart-' + self.id)) {
                        self.setChart();
                        window.addEventListener('resize', self.handleResize)
                        clearInterval(repeat)
                    }
                }, 300)
                let resizeRepeat = setInterval(function () {
                    if (document.getElementById('coordinate-chart-' + self.id)) {
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
                        var resizeDiv = document.getElementById('coordinate-chart-' + self.id);
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
                if(!document.getElementById('coordinate-chart-' + this.id)) return false;
                self.chart = echarts.init(document.getElementById('coordinate-chart-' + this.id));
                var hours = this.data.days;
                var days = this.data.labes;
                var data = this.data.data;
                let colors = ['#E96157', '#4FA5EB', '#3164FF'];
                data = data.map(function (item) {
                    return {
                        value: [item[1], item[0], item[2]],
                        itemStyle: {
                            normal: {
                                color: colors[Math.floor(Math.random() * 3)]
                            }
                        },
                    };
                });
                let assetOption = {
                    tooltip: {
                        position: 'top',
                        formatter:function (param) {
                            return '设备：'+days[param['value'][0]]+'</br>'+'时间：'+param.name+'</br>数目：'+self.changeWanUnit(param['value'][2]);
                        }
                    },
                    grid: {
                        left: 5,
                        bottom: 5,
                        right: 30,
                        top: 5,
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        data: hours,
                        boundaryGap: false,
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: 'rgba(0,0,0,0.1)',
                            }
                        },
                        axisLine: {
                            show: false
                        },
                        axisLabel: {
                            color: '#ddd'
                        }
                    },
                    yAxis: {
                        type: 'category',
                        data: days,
                        axisLine: {
                            show: false
                        },
                        axisLabel: {
                            color: '#9abcee'
                        }
                    },
                    series: [{
                        name: '设备情况',
                        type: 'scatter',
                        symbolSize: function (val) {
                            if (val[2]) {
                                return Math.floor(Math.random() * 15 + 20);
                            } else {
                                return 4;
                            }
                        },
                        data: data,
                        animationDelay: function (idx) {
                            return idx * 5;
                        }
                    }]
                };
                self.chart.setOption(assetOption);
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