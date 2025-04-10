declare module 'superagent-promise' {
    import * as superagent from 'superagent';

    function superagentPromise(
        superagent: any,
        Promise: PromiseConstructor
    ): typeof superagent;

    export = superagentPromise;
}
