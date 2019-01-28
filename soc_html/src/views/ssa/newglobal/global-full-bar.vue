<template>
    <div :id="'transfer-chart-'+id" :style="{width: width, height: height}"></div>
</template>
<style scoped>
</style>
<script>
    let echarts = require('echarts/lib/echarts');
    export default {
        name: "global-full-bar",
        props: {
            id: {
                default: 0
            },
            name: {
                default: ""
            },
            width: {
                default: "100%"
            },
            height: {
                default: "200px"
            },
            startColor: {
                default: ""
            },
            endColor: {
                default: ""
            },
            x: {
                default: function () {
                    return [];
                }
            },
            y: {
                default: function () {
                    return [];
                }
            },
	        need: {
                default: true
	        }
        },
        data() {
            return {
                chart: '',
            }
        },
        computed: {

        },
        watch: {
            'y': function () {
                this.initChart();
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
                self.chart = echarts.init(document.getElementById('transfer-chart-' + this.id));
                let xMax = Math.max.apply(null,self.x);
                let xData = [];
                for(let i in self.x){
                    xData.push(self.x[i]/xMax.toFixed(2)*100);
                }
                let option = {
                    grid: {
                        top: 10,
                        left: 0,
                        bottom: 0,
                        right: 0
                    },
                    xAxis: [{
                        axisTick: {
                            show: false,
                            // color:'#fff',
                        },
                        axisLine: {
                            show: false,
                        },
                        axisLabel: {
                            show: false
                                //color:'#fff',
                        },
                        splitLine: {
                            show: false,
                            // color:'#fff',
                        }
                    }],
                    yAxis: [{
                        type: 'category',
                        data: self.y,

                        axisTick: {
                            // color:'#fff',
                            show: false,
                        },
                        axisLine: {
                            //  color:'#fff',
                            show: false,
                        },
                        axisLabel: {
                            textStyle: {
                                color: '#fff',
                            },
                            inside: true
                        },
                        zlevel: 10

                    }],
                    series: [{
                        name: self.x,
                        type: 'bar',
                        barWidth: 22,
                        silent: true,
                        zlevel: 110,
                        itemStyle: {
                            normal: {
                                color: 'rgba(255,255,255,0.15)',
                                barBorderRadius: [0, 2, 2, 0],
                                label: {
                                    show: true,
                                    position: 'insideRight',
                                    formatter: function (val) {
                                        let str = '';
                                        if(self.need){
                                            str =  val.seriesName.split(',')[val.dataIndex] + '次'
                                        }else{
                                            str =  val.seriesName.split(',')[val.dataIndex]
                                        }
                                        return  str
                                    }
                                }
                            }
                        },
                        barGap: '-100%',
                        barCategoryGap: '50%',
                        data: self.x.map(function(d) {
                            return 100
                        }),
                    }, {
                        name: ' ',
                        type: 'bar',
                        barWidth: 22,
                        label: {
                            normal: {
                                show: false,
                                position: 'top',
                                formatter: '{c}%',
                            }
                        },
                        itemStyle: {
                                normal: {
                                    barBorderRadius: [0, 2, 2, 0],
                                    color: {
                                        type: 'bar',
                                        colorStops: [{
                                            offset: 0,
                                            color: self.startColor// 0% 处的颜色
                                        }, {
                                            offset: 1,
                                            color: self.endColor // 100% 处的颜色
                                        }],
                                        globalCoord: false, // 缺省为 false

                                    }
                                }
                        },
                        data: xData
                    }]
                };
                self.chart.setOption(option);
                window.addEventListener('resize', self.handleResize)
            },
            handleResize() {
                this.chart.resize();
            },
        },
    }
</script>