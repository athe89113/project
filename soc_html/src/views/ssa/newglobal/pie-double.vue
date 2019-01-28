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
                <div id="double-chart-{{ id }}"
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
        name: "double-chart",
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
                default: ''
            },
            unit: {
                default: ''
            },
            safeStatic:{
                default: ''
            }
        },
        data() {
            return {
                colors: ['#00BD85', '#4A92FF', '#D5B256', '#E96157', '#9abcee'],
            }
        },
        computed: {
            status: function () {
                 //0 加载之前   1 加载后无数据   2 加载后有数据
                if (this.safeStatic === "") {
                    return 0
                } else {
                    if (this.safeStatic != '{}') {
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
                    if (document.getElementById('double-chart-' + self.id)) {
                        self.setChart();
                        window.addEventListener('resize', self.handleResize)
                        clearInterval(repeat)
                    }
                }, 300)
                let resizeRepeat = setInterval(function () {
                    if (document.getElementById('double-chart-' + self.id)) {
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
                        var resizeDiv = document.getElementById('double-chart-' + self.id);
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
                if(!document.getElementById('double-chart-' + this.id)) return false;
                self.chart = echarts.init(document.getElementById('double-chart-' + this.id));
                function getData(percent, color, name) {
                    if(percent == 'NaN') percent = 0;
                    return [{
                        value: percent,
                        name: name,
                        itemStyle: {
                            normal: {
                                color: color
                            }
                        }
                    }, {
                        value: 1 - percent,
                        name:'bin',
                        itemStyle: {
                            normal: {
                                color: 'rgba(0,0,0,0.2)'
                            }
                        }
                    }];
                }
                let total = Number(self.safeStatic.low) + Number(self.safeStatic.mid) + Number(self.safeStatic.high) +Number(self.safeStatic.super);
                let staticOption = {
                    tooltip: {
                        trigger: 'item',
                        formatter: function (params, ticket, callback) {
                            if(params.name != 'bin') {
                                let value = 0;
                                if(params.name == '低危') value = self.safeStatic.low;
                                if(params.name == '中危') value = self.safeStatic.mid;
                                if(params.name == '高危') value = self.safeStatic.high;
                                if(params.name == '危急') value = self.safeStatic.super;
                                return params.seriesName + ": "+ value+'</br>占比：' + parseInt(params.value * 100)  + "%";
                            }
                        }
                    },
                    legend: {
                        top: "30%",
                        right: "15%",
                        data: ['低危', '中危', '高危', '危急'],
                        textStyle: {
                            color: '#fff'
                        },
                        selectedMode: true,
                        orient: "vertical",
                    },
                    series: [{
                        name: '低危',
                        type: 'pie',
                        clockWise: true, //顺时加载
                        hoverAnimation: false, //鼠标移入变大
                        radius: [65, 70],
                        center: ['30%', '50%'],
                        itemStyle: {
                            normal: {
                                color: '#00BD85',
                                label: {
                                    show: false,
                                },
                                labelLine: {
                                    show: false,
                                }
                            }
                        },
                        data: getData(parseFloat(self.safeStatic.low / total).toFixed(2), '#00BD85', '低危')
                    }, {
                        name: '中危',
                        type: 'pie',
                        clockWise: true, //顺时加载
                        hoverAnimation: false, //鼠标移入变大
                        radius: [50, 55],
                        center: ['30%', '50%'],
                        itemStyle: {
                            normal: {
                                color: '#4A92FF',
                                label: {
                                    show: false,
                                },
                                labelLine: {
                                    show: false,
                                }
                            }
                        },
                        data: getData(parseFloat(self.safeStatic.mid / total).toFixed(2), '#4A92FF', '中危')
                    }, {
                        name: '高危',
                        type: 'pie',
                        clockWise: true, //顺时加载
                        hoverAnimation: false, //鼠标移入变大
                        radius: [35, 40],
                        center: ['30%', '50%'],
                        itemStyle: {
                            normal: {
                                color: '#F89D44',
                                label: {
                                    show: false,
                                },
                                labelLine: {
                                    show: false,
                                }
                            }
                        },
                        data: getData(parseFloat(self.safeStatic.high / total).toFixed(2), '#F89D44', '高危')
                    }, {
                        name: '危急',
                        type: 'pie',
                        clockWise: true, //顺时加载
                        hoverAnimation: false, //鼠标移入变大
                        radius: [20, 25],
                        center: ['30%', '50%'],
                        itemStyle: {
                            normal: {
                                color: '#E96157',
                                label: {
                                    show: false,
                                },
                                labelLine: {
                                    show: false,
                                }
                            }
                        },
                        data: getData(parseFloat(self.safeStatic.super / total).toFixed(2), '#E96157', '危急')
                    }]
                };
                self.chart.setOption(staticOption);
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