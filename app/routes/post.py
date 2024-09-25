from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models.post import Post
from ..models.feedback import Feedback  
from ..forms import OrganizerForm, ParticipantsForm
from ..models.user import User

post = Blueprint('post', __name__)

# @post.route('/post/all', methods=['POST', 'GET'])
# def all(): 
#     posts = Post.query.order_by(Post.date).all()
#     return render_template('post/all.html', posts=posts, user=User)

@post.route('/', methods=['POST', 'GET'])
def all():
    form = OrganizerForm()
    form.organizer.choices = [t.name for t in User.query.filter_by(status='admin')]

    if request.method == "POST":
        organizer = request.form.get('organizer')
        organizer_id = User.query.filter_by(name=organizer).first().id
        posts = Post.query.filter_by(organizer=organizer_id).order_by(Post.date.desc()).all()
    else:
        posts = Post.query.order_by(Post.date.desc()).limit(35).all()
    return render_template('post/all.html', posts=posts, user=User, form=form)

@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    
    form = ParticipantsForm()
    form.participants.choices = [i.name for i in User.query.filter_by(status='user')]
    
    if request.method == "POST":
        # organizer = request.form.get('organizer')
        subject = request.form.get('subject')
        participants = request.form.get('participants')
        participant_id = User.query.filter_by(name=participants).first().id
        print(participant_id)
        post = Post(organizer=current_user.id, subject=subject, participants=participant_id)
        
        
        try:
            db.session.add(post)
            db.session.commit()            
            return redirect('/')
        except Exception as e:
            print(str(e))
        
    else:
        return render_template('post/create.html', form=form)
    

@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = Post.query.get(id)
    form = ParticipantsForm()
    form.participants.data = User.query.filter_by(id=post.participants).first().name
    form.participants.choices = [s.name for s in User.query.filter_by(status='user')]
    
    if post.author.id == current_user.id:
        if request.method == "POST":        
            # post.organizer = request.form.get('organizer')
            post.subject = request.form.get('subject')
            act_user = request.form.get('participants')
            post.participants = User.query.filter_by(name=act_user).first().id
            
            try:            
                db.session.commit()            
                return redirect(url_for('post.all'))
            except Exception as e:
                print(str(e))                
            
        else:
            return render_template('post/update.html', post = post, form = form)
    else:
        abort(403)

   
@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Post.query.get(id)        
    if post.author.id == current_user.id:           
        try:
            db.session.delete(post)            
            db.session.commit()            
            return redirect(url_for('post.all'))
        except Exception as e:
            print(str(e))
            return str(e)                
    else:
        abort(403)    

@post.route('/post/<int:id>/feedback', methods=['POST', 'GET'])
@login_required
def feedback(id):   
    
    if request.method == "POST":
        
        post_id = Post.query.get(id).id    
        author = current_user.id
        post_author_id =  Post.query.get(id).organizer  
        comment = request.form.get('text')        
        feedback = Feedback(post_id=post_id, author=author, post_author_id=post_author_id, comment=comment)
        
        
        # act_user = 5
        # list = Feedback.query.filter_by(post_author_id=act_user).all().get(comment)
        # user = db.session.query(Users).filter(Users.username == f'{username}').all()
        # list = Feedback.query.filter_by(post_author_id=act_user).all()
        # feedb = []
        # for i in list:
        #     feedb.append(i.comment)
        # print(feedb)
        # print(list)        
        # return redirect('/')
                
        try:
            db.session.add(feedback)
            db.session.commit()            
            return redirect('/')
        except Exception as e:
            print(str(e))
        
    else:
        return render_template('comment/feedback.html')    
    
               