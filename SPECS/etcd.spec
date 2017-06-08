%global with_devel 0
%global with_bundled 1
%global with_debug 1
%global with_check 0
%global with_unit_test 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
%endif

%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            etcd
# https://github.com/coreos/etcd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          d267ca9c184e953554257d0acdd1dc9c47d38229
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global system_name     etcd

Name:		etcd
Version:	3.1.8
Release:	1%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	%{system_name}.service
Source2:	%{system_name}.conf
Patch2:         0001-change-import-paths.patch
Patch3:         bz1350875-disaster-recovery-with-copies.patch
Patch4:         expand-etcd-arch-validation.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:x86_64 aarch64 ppc64le s390x}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

Obsoletes: etcd3 < 3.0.15
Provides: etcd3 = %{version}-%{release}

%if ! 0%{?with_bundled}
BuildRequires: golang(github.com/akrennmair/gopcap)
BuildRequires: golang(github.com/bgentry/speakeasy)
BuildRequires: golang(github.com/boltdb/bolt)
BuildRequires: golang(github.com/cheggaaa/pb)
BuildRequires: golang(github.com/cockroachdb/cmux)
BuildRequires: golang(github.com/codegangsta/cli)
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/coreos/go-systemd/daemon)
BuildRequires: golang(github.com/coreos/go-systemd/util)
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/dustin/go-humanize)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/google/btree)
BuildRequires: golang(github.com/jonboulle/clockwork)
BuildRequires: golang(github.com/kr/pty)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/prometheus/procfs)
BuildRequires: golang(github.com/spacejam/loghisto)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/ugorji/go/codec)
BuildRequires: golang(github.com/xiang90/probing)
BuildRequires: golang(golang.org/x/crypto/bcrypt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/http2)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/credentials)
BuildRequires: golang(google.golang.org/grpc/grpclog)
BuildRequires: golang(google.golang.org/grpc/transport)
%else
BuildRequires: libpcap-devel
%endif

BuildRequires:	systemd

Requires(pre):	shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A highly-available key value store for shared configuration.

%if 0%{?with_devel}
%package devel
Summary:        etcd golang devel libraries
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires: golang(github.com/cheggaaa/pb)
BuildRequires: golang(github.com/bgentry/speakeasy)
BuildRequires: golang(github.com/boltdb/bolt)
BuildRequires: golang(github.com/cockroachdb/cmux)
BuildRequires: golang(github.com/codegangsta/cli)
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/coreos/go-systemd/daemon)
BuildRequires: golang(github.com/coreos/go-systemd/util)
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/dustin/go-humanize)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/google/btree)
BuildRequires: golang(github.com/jonboulle/clockwork)
BuildRequires: golang(github.com/kr/pty)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/prometheus/procfs)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/ugorji/go/codec)
BuildRequires: golang(github.com/xiang90/probing)
BuildRequires: golang(golang.org/x/crypto/bcrypt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/http2)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/credentials)
BuildRequires: golang(google.golang.org/grpc/grpclog)
%endif

Requires: golang(github.com/cheggaaa/pb)
Requires: golang(github.com/bgentry/speakeasy)
Requires: golang(github.com/boltdb/bolt)
Requires: golang(github.com/cockroachdb/cmux)
Requires: golang(github.com/codegangsta/cli)
Requires: golang(github.com/coreos/go-semver/semver)
Requires: golang(github.com/coreos/go-systemd/daemon)
Requires: golang(github.com/coreos/go-systemd/util)
Requires: golang(github.com/coreos/pkg/capnslog)
Requires: golang(github.com/dustin/go-humanize)
Requires: golang(github.com/ghodss/yaml)
Requires: golang(github.com/gogo/protobuf/proto)
Requires: golang(github.com/google/btree)
Requires: golang(github.com/jonboulle/clockwork)
Requires: golang(github.com/kr/pty)
Requires: golang(github.com/olekukonko/tablewriter)
Requires: golang(github.com/prometheus/client_golang/prometheus)
Requires: golang(github.com/prometheus/procfs)
Requires: golang(github.com/spf13/cobra)
Requires: golang(github.com/spf13/pflag)
Requires: golang(github.com/ugorji/go/codec)
Requires: golang(github.com/xiang90/probing)
Requires: golang(golang.org/x/crypto/bcrypt)
Requires: golang(golang.org/x/net/context)
Requires: golang(golang.org/x/net/http2)
Requires: golang(google.golang.org/grpc)
Requires: golang(google.golang.org/grpc/codes)
Requires: golang(google.golang.org/grpc/credentials)
Requires: golang(google.golang.org/grpc/grpclog)

Provides: golang(%{import_path}/alarm) = %{version}-%{release}
Provides: golang(%{import_path}/auth) = %{version}-%{release}
Provides: golang(%{import_path}/auth/authpb) = %{version}-%{release}
Provides: golang(%{import_path}/client) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/concurrency) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/integration) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/mirror) = %{version}-%{release}
Provides: golang(%{import_path}/compactor) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/recipes) = %{version}-%{release}
Provides: golang(%{import_path}/discovery) = %{version}-%{release}
Provides: golang(%{import_path}/e2e) = %{version}-%{release}
Provides: golang(%{import_path}/error) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv2) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv2/command) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv3) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv3/command) = %{version}-%{release}
Provides: golang(%{import_path}/etcdmain) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v2http) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v2http/httptypes) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v3rpc) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v3rpc/rpctypes) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/auth) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/etcdserverpb) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/membership) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/stats) = %{version}-%{release}
Provides: golang(%{import_path}/integration) = %{version}-%{release}
Provides: golang(%{import_path}/lease) = %{version}-%{release}
Provides: golang(%{import_path}/lease/leasehttp) = %{version}-%{release}
Provides: golang(%{import_path}/lease/leasepb) = %{version}-%{release}
Provides: golang(%{import_path}/mvcc) = %{version}-%{release}
Provides: golang(%{import_path}/mvcc/backend) = %{version}-%{release}
Provides: golang(%{import_path}/mvcc/mvccpb) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/adt) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/contention) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/crc) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/expect) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fileutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/flags) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/httputil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/idutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ioutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/logutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mock/mockstorage) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mock/mockstore) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mock/mockwait) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/netutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/osutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pathutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pbutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/schedule) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/testutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/tlsutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/transport) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/wait) = %{version}-%{release}
Provides: golang(%{import_path}/proxy/httpproxy) = %{version}-%{release}
Provides: golang(%{import_path}/proxy/tcpproxy) = %{version}-%{release}
Provides: golang(%{import_path}/raft) = %{version}-%{release}
Provides: golang(%{import_path}/raft/raftpb) = %{version}-%{release}
Provides: golang(%{import_path}/raft/rafttest) = %{version}-%{release}
Provides: golang(%{import_path}/rafthttp) = %{version}-%{release}
Provides: golang(%{import_path}/snap) = %{version}-%{release}
Provides: golang(%{import_path}/snap/snappb) = %{version}-%{release}
Provides: golang(%{import_path}/store) = %{version}-%{release}
Provides: golang(%{import_path}/tools/benchmark/cmd) = %{version}-%{release}
Provides: golang(%{import_path}/tools/functional-tester/etcd-agent/client) = %{version}-%{release}
Provides: golang(%{import_path}/version) = %{version}-%{release}
Provides: golang(%{import_path}/wal) = %{version}-%{release}
Provides: golang(%{import_path}/wal/walpb) = %{version}-%{release}

%description devel
golang development libraries for etcd, a highly-available key value store for
shared configuration.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
#%setup -q -n %{repo}-%{commit}
%setup -q -n %{repo}-%{version}
# move content of vendor under Godeps as has been so far
mkdir -p Godeps/_workspace/src
mv cmd/vendor/* Godeps/_workspace/src/.

%if ! 0%{?with_bundled}
%patch2 -p1
%endif

%patch3 -p1
%patch4 -p1

%build
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/etcd

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?with_debug}
export LDFLAGS="-X %{import_path}/version.GitSHA=%{shortcommit}"
%else
export LDFLAGS="-X %{import_path}/version.GitSHA=%{shortcommit} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
%endif

%gobuild -o bin/%{system_name} %{import_path}
%gobuild -o bin/%{system_name}ctl %{import_path}/%{system_name}ctl

%install
install -D -p -m 0755 bin/%{system_name} %{buildroot}%{_bindir}/%{system_name}
install -D -p -m 0755 bin/%{system_name}ctl %{buildroot}%{_bindir}/%{system_name}ctl
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{system_name}.service
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{system_name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{system_name} %{SOURCE2}

# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{system_name}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

export BIN_PATH="$(pwd)/bin"

%gotest %{import_path}/client
%gotest %{import_path}/clientv3
%gotest %{import_path}/clientv3/integration
%gotest %{import_path}/compactor
%gotest %{import_path}/contrib/raftexample
%gotest %{import_path}/discovery
#%%gotest %%{import_path}/e2e
%gotest %{import_path}/error
%gotest %{import_path}/etcdctl/command
%gotest %{import_path}/etcdmain
%gotest %{import_path}/etcdserver
%gotest %{import_path}/etcdserver/auth
#%gotest %{import_path}/etcdserver/etcdhttp
#%gotest %{import_path}/etcdserver/etcdhttp/httptypes
#%%gotest %%{import_path}/integration
%gotest %{import_path}/lease
%gotest %{import_path}/pkg/adt
%gotest %{import_path}/pkg/cors
%gotest %{import_path}/pkg/crc
%gotest %{import_path}/pkg/fileutil
%gotest %{import_path}/pkg/flags
%gotest %{import_path}/pkg/idutil
%gotest %{import_path}/pkg/ioutil
%gotest %{import_path}/pkg/logutil
%gotest %{import_path}/pkg/netutil
%gotest %{import_path}/pkg/osutil
%gotest %{import_path}/pkg/pathutil
%gotest %{import_path}/pkg/pbutil
%gotest %{import_path}/pkg/schedule
%gotest %{import_path}/pkg/testutil
%gotest %{import_path}/pkg/transport
%gotest %{import_path}/pkg/types
%gotest %{import_path}/pkg/wait
%gotest %{import_path}/proxy
%gotest %{import_path}/raft
%gotest %{import_path}/raft/rafttest
%gotest %{import_path}/rafthttp
%gotest %{import_path}/snap
%gotest %{import_path}/storage
%gotest %{import_path}/storage/backend
%gotest %{import_path}/store
%gotest %{import_path}/tools/functional-tester/etcd-agent
%gotest %{import_path}/version
%gotest %{import_path}/wal
%endif

%pre
getent group %{system_name} >/dev/null || groupadd -r %{system_name}
getent passwd %{system_name} >/dev/null || useradd -r -g %{system_name} -d %{_sharedstatedir}/%{system_name} \
	-s /sbin/nologin -c "etcd user" %{system_name}

%post
%systemd_post %{system_name}.service

%preun
%systemd_preun %{system_name}.service

%postun
%systemd_postun %{system_name}.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc *.md
%doc glide.lock
%config(noreplace) %{_sysconfdir}/%{system_name}
%{_bindir}/%{system_name}
%{_bindir}/%{system_name}ctl
%dir %attr(-,%{system_name},%{system_name}) %{_sharedstatedir}/%{system_name}
%{_unitdir}/%{system_name}.service

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc *.md
%doc glide.lock
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%license LICENSE
%doc *.md
%endif

%changelog
* Thu Jun 08 2017 Jan Hiroaki Nakamura <hnakamur@gmail.com> - 3.1.8-1
- Update to 3.1.8

* Tue May 02 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.7-1
- Update to 3.1.7
  resolves: #1447235

* Tue Apr 04 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 3.1.3-2
- Circumvent runtime check of officially supported architectures
  resolves: #1434973

* Tue Mar 21 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.3-1
- Update to 3.1.3
  resolves: #1434364

* Mon Feb 27 2017 Josh Boyer <jwboyer@redhat.com> - 3.1.0-2.1
- Rebuild rebase on all architectures

* Tue Feb 21 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.0-2
- Apply "add --keep-cluster-id and --node-id to 'etcdctl backup'"
  from extras-rhel-7.2 branch
  resolves: #1350875

* Thu Feb 16 2017 Josh Boyer <jwboyer@redhat.com> - 3.1.0-1.1
- Rebuild rebase on all architectures

* Mon Feb 06 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.0-1
- Update to 3.1.0
  etcdctl-top removed by upstream
  resolves: #1416440

* Fri Jan 20 2017 d.marlin <dmarlin@redhat.com>
- Build for all archs (adding ppc64le and s390x)

* Tue Jan 10 2017 d.marlin <dmarlin@redhat.com> 
- Add aarch64 to ExclusiveArch list.

* Mon Jan 09 2017 d.marlin <dmarlin@redhat.com> 
- Correct 'link' warning for -X flag.

* Thu Dec 01 2016 jchaloup <jchaloup@redhat.com> - 3.0.15-1
- Update to 3.0.15
  Obsolete etcd3 < 3.0.15

* Fri Nov 18 2016 jchaloup <jchaloup@redhat.com> - 3.0.14-3
- Build with debug-info subpackage
- Until etcd3 obsoletes etcd it conflicts with it

* Tue Nov 15 2016 Avesh Agarwal <avagarwa@redhat.com> - 3.0.14-2
- Resolves: #1395359 etcd3 should not obsolete etcd

* Mon Nov 07 2016 jchaloup <jchaloup@redhat.com> - 3.0.14-1
- Update to v3.0.14
  related: #1386963

* Thu Oct 27 2016 jchaloup <jchaloup@redhat.com> - 3.0.13-1
- Update to v3.0.13
  related: #1386963

* Fri Oct 21 2016 jchaloup <jchaloup@redhat.com> - 3.0.12-3
- etcdctl: fix migrate in outputing client.Node to json
  resolves: #1386963

* Tue Oct 18 2016 jchaloup <jchaloup@redhat.com> - 3.0.12-2
- Replace etcd with etcd3 when upgrading
  resolves: #1384161

* Thu Oct 13 2016 jchaloup <jchaloup@redhat.com> - 3.0.12-1
- Update to v3.0.12

* Thu Oct 06 2016 jchaloup <jchaloup@redhat.com> - 3.0.10-1
- Update to v3.0.10

* Fri Sep 23 2016 jchaloup <jchaloup@redhat.com> - 3.0.3-2
- Extend etcd.conf with new flags
  resolves: #1378706

* Fri Jul 22 2016 jchaloup <jchaloup@redhat.com> - 3.0.2-1
- Update to v3.0.3
  related: #1347499

* Tue Jul 12 2016 jchaloup <jchaloup@redhat.com> - 3.0.2-1
- Update to v3.0.2
  related: #1347499

* Sun May 15 2016 jchaloup <jchaloup@redhat.com> - 3.0.0-0.1.beta0
- Build etcd3 v3.0.0-beta0 for AH 7.3
  resolves: #1347499
