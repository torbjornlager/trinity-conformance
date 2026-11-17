// Opt-in diagnostic: real WASM parent/child actors, mocked remote HTTP answer.
// Run with SWI_WASM_TEST_HOST pointing here and the named scenario below.
exports.cases = ({PID,CLIENT,behaviourSource,startToplevel,scopedWorkerCoordinator,deliver,until}) => ({
  async appendix_promise_context_parent_child(W,check) {
    const host=scopedWorkerCoordinator(W);
    host.requestSwiWasmWorkerRpc=()=>Promise.resolve('success([v(ok)],false).');
    try {
      await startToplevel(W,undefined,behaviourSource,'shell_toplevel');
      const goal="promise('https://example.org',X=ok,Ref,[template(v(X))]),self(Parent),"+
        "spawn((catch(yield(Ref,Answer),Error,Answer=error(Error)),send(Parent,context_result(Answer))),Child,[monitor(true)]),"+
        "receive({context_result(Observed)->true},[timeout(3),on_timeout(throw(missing_context_result))]),"+
        "receive({down(Child,Child,true)->true},[timeout(3),on_timeout(throw(missing_context_child_down))]),promise_cleanup(Ref)";
      const replies=()=>W.sends.filter(m=>m.to===CLIENT).map(m=>m.message),before=replies().length;
      deliver(W,"'$call'(("+goal+"),[template(Observed)])");
      await until(()=>replies().length>before,6000);
      const answer=replies()[before]||'no answer';
      console.log('CONTEXT_OBSERVATION '+answer);
      check(answer.includes(',[success([v(ok)],false)],false)'),
        'a child in the same client context collects its parent promise: '+answer);
    } finally {await host.stop();}
  }
});
