/**
 * Created by david on 12/04/20.
 */
// Long Polling to update image
    function poll_png(){
        $.ajax({ url: "/get_frame_png_b64", success: function(data){
            $("#cam_image").attr("src", "data:image/png;base64,"+data);
            }, dataType: "text", complete: function(jqXHR, status){
                if (status == 'success') {poll_png();} else {console.log('Error during image polling, make sure server is up and try refreshing the page');}
            }, timeout: 30000 });
    }



    var _min = 0;
    var _max = 1e9;

    function map_array(data, cmin, cmax){
        out = new Uint8ClampedArray(data.length*4);

        //record min and max
        _min = 1e9;
        _max = 0;

        for (j = 0; j< data.length; j++){
            k = j*4;
            v = data[j];
            _min = Math.min(v, _min);
            _max = Math.max(v,_max);
            v = (v - cmin)/(cmax-cmin);
            //console.log(v)
            v_ = 255*v; //simple grayscale map - FIXME
            out[k] = v_;
            out[k+1] = v_;
            out[k+2] = v_;
            out[k+3] = 255; //alpha
        }

        return out
    }

    // Long Polling to update image
    function poll_array(){
        $.ajax({
            url: "/get_frame_pzf",
            success: function(data){
                //console.log(data);
                decoded = decode_pzf(data);
                //console.log(decoded);
                im = new ImageData(map_array(decoded.data, parseFloat($("#display_min").val()), parseFloat($("#display_max").val())), decoded.width, decoded.height);
                if ($("#display_autoscale").is(":checked")){
                    $("#display_min").val(_min);
                    $("#display_max").val(_max);
                }
                var zoom = parseFloat($("#display_zoom").val())/100.;
                var canvas = document.getElementById("cam_canvas");
                $("#cam_canvas").attr({width: decoded.width*zoom, height : decoded.height*zoom});
                var ctx = canvas.getContext('2d');
                //ctx.scale(zoom, zoom);

                createImageBitmap(im, options={resizeWidth: decoded.width*zoom, resizeHeight:decoded.height*zoom, resizeQuality:'pixelated'}).then(function(bmp){
                    ctx.drawImage(bmp, 0, 0);
                });
                //console.log(im);
                //ctx.putImageData(im, 0, 0);

                },
            //dataType: "text",
            complete: function(jqXHR, status){
                    if (status == 'success') {poll_array();} else {console.log('Error during image polling, make sure server is up and try refreshing the page');}
                },
            timeout: 30000,
            xhrFields: {responseType: 'arraybuffer'}
        });
    }

    poll_array();

    var scope_state = {};
    scope_state['Camera.IntegrationTime']=0.1 //default start option

    var app = new Vue({
        el: '#app',
        data: {
            message: 'Hello Vue!',
            state: scope_state
            }
    });

    function update_server_state(state){
        //console.log('updating state', state);
        $.ajax({
            url : "/update_scope_state",
            data : JSON.stringify(state),
            processData: false,
            type: 'POST',
            error: function(jqXHR, textStatus, errorThrown){
                console.log("failed to update state");
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    }

    var hw = new Vue({
        el: '#hw',
        data: {
            message: 'Hello Vue!',
            state: scope_state

            },
        computed: {
            integration_time_ms: function () {
                return this.state['Camera.IntegrationTime']*1000;
                },

            laser_names: function () {
                lks = Object.keys(this.state).filter(function(key){return key.startsWith('Lasers') && key.endsWith('On');})
                laser_info = lks.map(function(k){
                    lname= k.split('.')[1];
                    return lname;
                });
                return laser_info;
                }
            },
        methods:{
            update_server_state : update_server_state,
            set_laser_power: function(lname, value){var key = 'Lasers.' + lname + '.Power';
                                            var state = {};
                                            state[key] = parseFloat(value);
                                            update_server_state(state);} ,
            set_laser_on: function(lname, value){var key = 'Lasers.' + lname + '.On';update_server_state({key: value});},
        }
    });

    function get_state(){
        $.ajax({
            url: "/get_scope_state",
            success: function(data){
                app.state=data;
                hw.state = data;
                //$("#int_time").val(1000*app.state['Camera.IntegrationTime'])
            }

        })
    }

    get_state();

    function poll_state(){
        $.ajax({
            url: "/scope_state_longpoll",
            success: function(data){ console.log(data);
                app.state=data;
                hw.state = data;
                //$("#int_time").val(1000*app.state['Camera.IntegrationTime'])
            },
            complete: function(jqXHR, status){
                    if (status == 'success') {poll_state();} else {console.log('Error during image polling, make sure server is up and try refreshing the page');}
                }

        })
    }

    poll_state();


    $(window).on('load', function(){$("#home-tab").tab('show');});