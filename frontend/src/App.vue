<template>
  <div id="app">

    <app-header class="head"></app-header>
    <app-Menu class="menu"></app-Menu>
    <app-Upload @add="add(arguments)"></app-Upload>
    <app-Table @add="add(arguments)"></app-Table>
    <app-Code @add="add(arguments)"></app-Code>
    <app-Transmit @add="add(arguments)"></app-Transmit>
    <app-Log ref="logcontainer"></app-Log>
    <app-footer style="margin-top:50px"></app-footer>

  </div>
</template>

<script>
import Header from "./components/Header";
import Footer from "./components/Footer";
import Table from "./components/Table"
import Menu from "./components/Menu";
import Upload from "./components/Upload"
import Code from "./components/Code"
import Transmit from "./components/Transmit"
import Log from "./components/Log"
export default {
  name: 'App',
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    "app-footer": Footer,
    "app-Menu": Menu,
    "app-Table":Table,
    "app-Upload" :Upload,
    "app-Code":Code,
    "app-Transmit":Transmit,
    "app-Log":Log,
  },
  methods : {
    add(block,msg){
      this.$refs.logcontainer.add_log(block,msg);
    }
  },
};
</script>

<style scoped>

.menu{ 
    position: fixed;
  }
.head{
  background-color: #e9eef3;
}
</style>
