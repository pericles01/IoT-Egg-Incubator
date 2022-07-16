<template>
  <v-container fluid>
      <v-sheet 
      color="white"
      elevation="3">
        <v-container>
          <div class="picture1">
            <v-row>
              <v-col
                cols="6" col-md="12"
              > 
                <v-gauge :value="value1" unit="°C" top></v-gauge>
                <h2> Temperature </h2>
              </v-col>
              <v-col
                cols="6"
                col-md="12"
              >
                <v-gauge :value="value2" unit="%" top></v-gauge>
                <h2> Humidity </h2>
              </v-col>
            </v-row>
          </div>
        </v-container>
      </v-sheet>
      <v-sheet 
      color="grey lighten-3">
        <div class="swichin">
          <v-container>
            <v-row>
              <v-col cols="12" col-md="12" class="">
                <v-switch
                  v-model="switch1"
                  inset
                  :label="`Heater`"
                  color="red"
                  @change="controlHeater"
                ></v-switch>
                <v-switch
                  v-model="switch2"
                  inset
                  :label="`Humidifier`"
                  @change="controlHumidifier"
                > </v-switch>

                <v-switch
                  v-model="switch3"
                  inset
                  :label="`1/4 Motor turn`"
                  color="green"
                  @change="controlMotor"
                > </v-switch>
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-sheet>
      <v-spacer></v-spacer>
      <v-sheet 
      elevation="5"
      color="white"
      >
        <div class="formulaire">
          <v-form>
            <v-container>
                <v-row>
                  <v-col
                    cols="6"
                    col-md="12"
                  >
                    <v-text-field
                      v-model="temp"
                      label="Set temperature"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>

                  <v-col
                    cols="6"
                    col-md="12"
                  >
                    <v-text-field
                      v-model="hum"
                      label="Set humidity"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" col-md="12">
                    <v-btn
                      class="mx-auto"
                      color="primary"
                      elevation="4"
                      @click="startJob"
                    > Start the job </v-btn>
                  </v-col>
                </v-row>
            </v-container>
          </v-form>
        </div>
      </v-sheet>
  </v-container>
</template>

<script>
  import axios from 'axios';
  import VGauge from 'vgauge';
  //import Chart from 'chart.js'

  export default {
    name: 'HelloWorld',
    components: {
      VGauge
    },

    data: () => ({
      switch1: false,
      switch2: false,
      switch3: false,
      temp: 30,
      hum: 40,
      value1: 35 ,
      value2: 40 ,
      ip: '192.168.2.160:5000',
      //dataPlot: null,
      //maxDataPoints: 20,
    }),
    methods:{
      /*
      removeData(){
        let that = this;
        that.dataPlot.data.labels.shift();
        that.dataPlot.data.datasets[0].data.shift();
        that.dataPlot.data.datasets[1].data.shift();
      },
      addData(label, data1, data2) {
        let that = this;
        if(that.dataPlot.data.labels.length > that.maxDataPoints) that.removeData();
        that.dataPlot.data.labels.push(label);
        that.dataPlot.data.datasets[0].data.push(data1);
        that.dataPlot.data.datasets[1].data.push(data2);
        that.dataPlot.update();
      },
      */
      datastream(){
        let that = this;
        const url ='ws://'+that.ip+'/data';
        let connection = new WebSocket(url);
        /*
        that.dataPlot = new Chart(document.getElementById("line-chart"), {
            type: 'line',
            data: {
              labels: [],
              datasets: [
                {
                  data: [],
                  label: "Temperature (°C)",
                  borderColor: "#3e95cd",
                  fill: false
                },
                {
                  data: [],
                  label: "Humidity (%)",
                  borderColor: "#8e5ea2",
                  fill: false
                }
              ]
            }
          });
        */
        connection.onmessage = (event) => {
          let msg = event.data;
          msg = msg.replaceAll('\'', '"');
          
          msg = JSON.parse(msg);
          let x = msg.temperature;
          that.value1 = parseFloat(x) ; 
          let y = msg.humidity;
          that.value2 = parseFloat(y) ;
          console.log("response datastream websocket")
          console.log(msg)
          console.log(typeof(msg))
          console.log({'temp': that.value1, 'hum': that.value2})
          /*
          let today = new Date();
          let t = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
          that.addData(t, that.value1, that.value2);
          */
        };
      },
  
      controlHeater(){
        let that = this
        const url ='http://'+that.ip+'/controlHeater';
        let data = {};
        if(that.switch1)
          data = {state: 1};
        else
          data = {state: 0};
        console.log(data)
        axios.put(url, data)
          .then((response) => {
            console.log("response api control heater")
            console.log(response)
            })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },

      controlHumidifier(){
        let that = this
        const url ='http://'+that.ip+'/controlHumidifier';
        let data = {}
        if(that.switch2)
          data = {'state' : 1};
        else
          data = {'state': 0};
        console.log(data)
        axios.put(url, data)
          .then((response) => {
            console.log("response api control humidifier")
            console.log(response)
            })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },

      controlMotor(){
        let that = this
        const url ='http://'+that.ip+'/controlMotor';
        let data = {}
        if(that.switch3)
          data = {state : 1};
        else
          data = {state: 0};
        console.log(data)
        axios.put(url, data)
          .then((response) => {
            console.log("response api control motor")
            console.log(response)
            })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },

      startJob(){
        let that = this
        const url ='http://'+that.ip+'/job';
        let temperature = parseFloat(that.temp);
        let humidity = parseFloat(that.hum);
        let data = {'setTemp' : temperature, 'setHum' : humidity};
        console.log(data)
        axios.put(url, data)
          .then((response) => {
            console.log("response api regulator-job")
            console.log(response)
            })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });

        alert("You have successfully started a new job");
      },


    },
    created(){
        this.datastream();
        this.controlHeater();
        this.controlHumidifier();
        this.controlMotor();
        //this.startJob();
      }
  };
</script>

<style>
  .picture1{
    text-align: center;
  }

  .swichin{
    text-align: center;
    position: center;
  }

  .formulaire{
    text-align: center;
  }
  /*
  .chart{
    text-align: center;
    position: center;
  }
  */

</style>