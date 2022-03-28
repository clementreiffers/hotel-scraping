import {spawn} from 'node:child_process';
import gulp from 'gulp';

const {watch, series} = gulp;

let myProcess = null;

const watcher = async () => {
    watch(['./**/*.csv'], series(stop, start));
};

const start = async () => {
    // myProcess = spawn('node', ['index.js'], {stdio: 'inherit'});
    console.log("on vient d'écrire dans un csv");
};

const stop = async () => {
    /*
    if (myProcess) {
        await myProcess.kill();
        myProcess = null;
    }*/
    console.log("j'arrete un processus");
};

const defaultRun = series(start, watcher);

export default defaultRun;
export {watcher, defaultRun};