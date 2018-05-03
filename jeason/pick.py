import pickle
class Foo(object): pass

a = Foo()
with open('../xmnlp/sentiment/sentiment.pickle','wb') as f:
  pickle.dump(a,f)
  print(f)