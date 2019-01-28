<template>
    <div class="pieBorder" :id="'transfer-chart-'+id" :style="{width: width, height: height}"></div>
</template>
<style scoped>
	/*.pieBorder{
		position: absolute;
		top: 0;
		left: 0;
		z-index: 2;
	}*/
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
            data: {
                default: function () {
                    return []
                }
            },
            x: {
                default: 'center'
            },
            y: {
                default: 'bottom'
            },
            position: {
                default: ['50%', '50%']
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
            'data': function () {
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
                var data = this.data, lable = [];
                data.forEach((item) => {
                    lable.push(item.name);
                });
                let option = {
                    title: {
                        text:data.length+'种',
                        y: '53%',
                        left: '30%',
                        textStyle: {
                            fontWeight: 'normal',
                            fontSize: 24,
                            color: "#fff",
                            fontFamily: 'AliHYAiHei-Beta',
                        }
                    },
                    tooltip: {
                        show: true,
                        trigger: 'item',
                        formatter: "{a} <br/>{b}: {c} ({d}%)"
                    },
                    legend: {
                        type: 'scroll',
                        orient: 'vertical',
                        right: '10%',
                        top: 'middle',
                        textStyle: {
                            color: 'rgba(216,216,216,1)'
                        },
                        itemWidth: 12,
                        itemHeight: 12,
                        pageIconColor: '#4ca370',
                        data: lable
                    },
                    series: [
                        {
                            name: '安全检查类别',
                            type: 'pie',
                            selectedMode: 'single',
                            center: ['35%', '60%'],
                            radius: ['50%', '60%'],
                            /*color: '#1DFF9E',*/
                            label: {
                                normal: {
                                    show: false,
                                },
                                emphasis: {
                                    position: 'inner',
                                    formatter: '{d}%',
                                    textStyle: {
                                        color: '#fff',
                                        fontSize: 12
                                    }
                                }
                            },
                            labelLine: {
                                normal: {
                                    show: false
                                }
                            },
                            itemStyle: {
                                normal: {
                                    borderWidth: 1,
                                    borderColor: '#000',
                                }
                            },
                            data: data
                        },
                        {
                            name: '安全检查类别',
                            type: 'pie',
                            center: ['35%', '50%'],
                            radius: ['60%', '75%'],
                            hoverAnimation: false,
                            itemStyle: {
                                normal: {
                                    color: 'rgba(0,0,0,0.2)'
                                },
                                emphasis: {
                                    color: 'rgba(0,0,0,0.4)'
                                }
                            },
                            label: {
                                normal: {
                                    show: false,
                                },
                                emphasis: {
                                    position: 'inner',
                                    formatter: '{c}',
                                    textStyle: {
                                        color: '#fff',
                                        fontSize: 12
                                    }
                                }
                            },
                            data: data
                        }]
                }
                self.chart.setOption(option);
                window.addEventListener('resize', self.handleResize)
            },
            handleResize() {
                this.chart.resize();
            },
        },
    }
</script>