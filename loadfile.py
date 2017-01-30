import os
import numpy as np
import tensorflow as tf

def weight_variable(shape):
	initial = tf.truncated_normal(shape,stddev=0.001)
	return tf.Variable(initial)
def bias_variable(shape):
	initial = tf.constant(0.0,shape=shape)
	return tf.Variable(initial)
def max_pool_2x2(x):
	return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
def conv2d(patch_x_size,patch_y_size,channel,number_of_output_channel,x):
	W = weight_variable([patch_x_size,patch_y_size,channel,number_of_output_channel])
	b = bias_variable([number_of_output_channel])
	hc = tf.nn.elu(tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')+b)
	return W,b,hc

def simple_nn(input_size,output_size,x):
	W = weight_variable([input_size,output_size])
	b = bias_variable([output_size])
	hc = tf.matmul(x,W)+b
	return W,b,hc
def simple_softmax(input_size,output_size,x):
	W = weight_variable([input_size,output_size])
	b = bias_variable([output_size])
	hc= tf.nn.softmax(tf.matmul(x,W)+b)
	return W,b,hc


def main():

	laststate_collectionname = r"c:\tf\baduk\laststate_kibotfcollection.npy"
	komi_collectionname = r"c:\tf\baduk\komi_kibotfcollection.npy"
	winner_collectionname = r"c:\tf\baduk\winner_kibotfcollection.npy"
	laststate = np.load(laststate_collectionname )
	komi = np.load(komi_collectionname )
	winner = np.load(winner_collectionname )

	laststate = laststate.reshape(177448*4,21*21*3)
	komi = komi.reshape(177448*4,1)
	winner = winner.reshape(177448*4,1)

	totnum = 177448


	winner_int = np.zeros((totnum*4),dtype=np.int32)
	for i in range(totnum*4):
		if winner[i,0]>0.5 :
			winner_int[i]=1
		else:
			winner_int[i]=0

	x = tf.placeholder(tf.float32,shape=[None,21*21*3 ])
	ko = tf.placeholder(tf.float32,shape=[None,1])
	y_= tf.placeholder(tf.int32,shape=[None])



	x_image = tf.reshape(x,[-1,21,21,3])
	keep_prob = 1.0#tf.placeholder(tf.float32)



	W1, b1, hc1 = conv2d(5, 5, 3, 16, x_image)
	#hp1 = max_pool_2x2(hc1)
	W2, b2, hc2 = conv2d(3, 3, 16, 32, hc1)
	#hp2 = max_pool_2x2(hc2)
	hp2flat = tf.reshape(hc2, [-1, 21 * 21 * 32])
	wfc1, bfc1, hf1 = simple_nn(21 * 21 * 32, 10, hp2flat)
	hfc1 = tf.nn.relu(hf1)

	hhh = tf.concat([hfc1,ko],1)
	#hfp1drop = tf.nn.dropout(hfc1, keep_prob)
	wfc2, bfc2, y_conv = simple_nn(11, 2, hhh)
	#W,b,hc=conv2d(patch_x_size,patch_y_size,channel,number_of_output_channel,x):

	sq2 =tf.nn.sparse_softmax_cross_entropy_with_logits(y_conv,y_)
	sq = tf.sqrt(tf.reduce_mean(tf.square( tf.subtract(y_conv , y_))))
	train_step = tf.train.AdamOptimizer(2e-4).minimize(sq2)



	init = tf.global_variables_initializer()
	saver = tf.train.Saver()


	sess = tf.Session()
	sess.run(init)

	#saver.restore(sess, r"c:\tf\baduk\bbb\model.ckpt")


	iterrange = 10000
	bs = 10000
	bn = (4*130000)//bs
	for iter in range(iterrange):
		if iter % 10 ==0:
			save_path= saver.save(sess,r"c:\tf\baduk\bbb\model.ckpt")

		for i in range(bn):
			start = i*bs
			end = (i+1)*bs
			sess.run(train_step,feed_dict={x:laststate[start:end,0:21*21*3],y_:winner[start:end,0:1]})


		tbn = (4*40000) // bs
		test=0
		for itertest in range(tbn):
			sqstart = 4*130000 + tbn*bs
			sqend = sqstart + bs
			test += sess.run(sq, feed_dict={x: laststate[sqstart:sqend, 0:21 * 21 * 3], y_: winner_int[sqstart:sqend, 0], ko:komi[sqstart:sqend, 0:1]})
		test = test/tbn
		print("iter %d step %d, trainning accuracy %f"%(iter,iterrange,test))

main()