# AlmaLinux version 9
FROM almalinux:9
MAINTAINER Antonio J. Delgado <antonio.delgado@csc.fi>
RUN yum clean all && \
    yum -y install epel-release && \
    yum -y groupinstall "Development tools" && \
    yum -y install python3.11-devel python3-mysql sshpass && \
    yum -y install acl sudo && \
    sed -i -e 's/^Defaults.*requiretty/Defaults    !requiretty/' -e 's/^%wheel.*ALL$/%wheel    ALL=(ALL)    NOPASSWD: ALL/' /etc/sudoers && \
    yum -y install python3.11-pyyaml python3.11-jinja2 python3-paramiko python3.11-setuptools git python3.11-pip && \
    /usr/bin/pip3.11 install pyrax pysphere boto passlib dnspython || /usr/bin/pip3.11 install pyrax pysphere boto passlib dnspython && \
    yum -y remove $(rpm -qa "*-devel") && \
    yum -y groupremove "Development tools" && \
    yum -y autoremove && \
    yum -y install bzip2 crontabs file findutils gem git gzip hg hostname procps-ng svn sudo tar tree which unzip xz zip

RUN mkdir /etc/ansible/
RUN echo -e '[local]\nlocalhost' > /etc/ansible/hosts
RUN /usr/bin/pip3.11 install cryptography==3.3 bcrypt==3.1.7 PyNaCl==1.3.0
RUN /usr/bin/pip3.11 install ansible==2.9.19
RUN ansible --version

CMD ["/bin/bash"]
