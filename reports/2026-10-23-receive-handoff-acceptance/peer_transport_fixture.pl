% Disposable loopback fixture; token is public test data, not a credential.
:- multifile distribution:hook_transport_options/2.
distribution:hook_transport_options('http://127.0.0.1:52080',[request_header('Authorization'='Bearer checkpoint-fixture-peer')]).
