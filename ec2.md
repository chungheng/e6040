# Using Amazon Machine Image with Preloaded Theano

## Setting up with Amazon EC2

A few links to [Amazon EC2 Documentation](http://aws.amazon.com/documentation/ec2/) are provided
here to help you set up with Amazon EC2. If you have already set up with Amazon EC2, you can skip
to the next section.

- [Amazon student](https://aws.amazon.com/education/awseducate/) provides $35 credit to students. 
- General information about Amazon EC2 can be found [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html).
- To sign up for AWS and prepare for launching an instance, follow the documentation [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html).
- To start an Amazon EC2 Linux instance, follow [these steps](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html).
- Make sure to check out these [best practice guides](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html) to better manage your instances.
- Make sure that you understand the [pricing information](https://aws.amazon.com/ec2/pricing/) for EC2 instances and storage.

If you follow these steps, the setup time usually takes 1-2 hours.

## Using Preloaded Amazon Machine Image

We made available a public Amazon Machine Image (AMI) in which all packages required by Theano
and Theano itself have been preloaded. The AMI is only available in US East Region currently,
and you must launch the AMI in this region. Please follow the steps below to launch an GPU
instance using the AMI.

First, change your region to US East and search in the public images for `E6040_AMI`. Click on
the one with AMI ID: ami-e3e3c689. Then click Launch button on the top.

![ec2-ami-1]('notebooks/files/ec2-ami-1.png')

You will be prompted to Step 2 of instance setup. 
Here, choose either `g2.2xlarge` for an instance with 1 GPU or `g2.8xlarge` for one with 4 GPUs.

![ec2-ami-2]('notebooks/files/ec2-launch-step2.png')

In step 3: leave the default setting for instance details, or customize it according to your needs.

In step 4, add storage with at least 8 GiB size. If you wish to keep the root storage, uncheck "Delete on Termination" box. Add additional storage as you need.
![ec2-ami-4]('notebooks/files/ec2-launch-step4.png')

In step 5, you can leave it as is or create a new tag for you instance.

In step 6, select an existing security group. Then, review and launch the instance. You can log into your instance by

```bash
ssh -i your-key.pem ubuntu@replace-ec2-DNS-here
```

Once you are logged in, actviate the Theano environment by:


```bash
source activate theano
```

Environment is managed by [Conda](http://conda.pydata.org/docs/) using miniconda2 installed
under `/home/ubuntu`. You can now start using Theano. Remember to terminate (not just stop)
the instance after use, otherwise you will be charged even if the instance is idling.

## Create Your Own AMI

If you install additional software packages on top of the provided AMI, and want to avoid
installing them again the next time you launch an instance, you can create an image on your
own instance. Details can be found [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html).

## Using Jupyter Notebook on the GPU instance

Jupyter has been preloaded on the AMI. To launch a notebook server, follow
the [instruction](http://jupyter-notebook.readthedocs.org/en/latest/public_server.html),
or do the following:

```bash
source activate theano
ipython
[ ... lauching ipython interpreter ... ]
```

```ipython
In [1]: from notebook.auth import passwd
In [2]: passwd()
```

Copy the output starting with `sha1:`.

Edit the file `~/.jupyter/jupyter_notebook_config.py` and paste the above output in between
the quotes on the line (uncomment the line by removing # at the beginning of the line):

```python
c.NotebookApp.password = ''
```
Create an self-assigned certificate to enable secure connection to the server

```bash
cd ~/
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mykey.key -out mycert.pem
```

Launch jupyter notebook

```bash
jupyter notebook
```

In your EC2 console, add a TCP rule to the security group that your instance is using.

![add-port]('notebooks/files/add_port.png')

You can now access the notebook server from your browser by enter the DNS address of your
instance, e.g.: `https://ec2-DNS:9999`. The default port is set to `9999`, this can be changed
in the file `~/.jupyter/jupyter_notebook_config.py`.