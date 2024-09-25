from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.post import Post
from ..models.feedback import Feedback
from ..forms import OrganizerForm, ParticipantsForm
from ..models.user import User
from ..functions import review, overall_rating

comment = Blueprint('comment', __name__)

@comment.route('/comment/administration', methods=['POST', 'GET'])
def administration():
        feedbacks = Feedback.query.distinct('post_author_id')
        list = []
        for i in feedbacks:
            list.append(i.post_author_id)
                    
        return render_template('comment/administration.html', feedbacks=feedbacks, user=User)
        
    # form = OrganizerForm()
    # form.organizer.choices = [s.name for s in User.query.filter_by(status='admin')]
    
    # if request.method == "POST":
    #     organizer = request.form.get('organizer')
    #     print()
    #     organizer_id = User.query.filter_by(name=organizer).first().id
    #     comms = Post.query.filter_by(organizer=organizer_id).order_by(Post.date.desc()).all()
    # else:
    #     comms = Post.query.order_by(Post.date.desc()).limit(35).all()       
            
    # return render_template('comment/administration.html', feedbacks=comms, user=User, form=form)

# @comment.route('/comment/administration', methods=['POST', 'GET'])
# @login_required
# def administration():
        
#     form = OrganizerForm()
#     form.organizer.choices = [s.name for s in User.query.filter_by(status='admin')]
    
#     if request.method == "POST":
#         organizer = request.form.get('organizer')
#         print()
#         organizer_id = User.query.filter_by(name=organizer).first().id
#         comms = Post.query.filter_by(organizer=organizer_id).order_by(Post.date.desc()).all()
#     else:
#         comms = Post.query.order_by(Post.date.desc()).limit(35).all()       
            
#     return render_template('comment/administration.html', feedbacks=comms, user=User, form=form)


@comment.route('/comment/<int:id>/work', methods=['POST', 'GET'])
def work(id):
    
    ratings = Feedback.query.filter_by(post_author_id=id).all() 
    id = id   
    list_comments = []
    list_review = []
    
    for post in ratings:
        list_comments.append(post.comment)
    
    for post in list_comments:
        list_review.append(review(post))
        
    feedback_raiting = dict(zip(list_comments, list_review))
    
    general_opinion = overall_rating(list_review)   
      
    return render_template('comment/rating.html', feedback_raiting=feedback_raiting, id = id, go = general_opinion )


@comment.route('/comment/<int:author_id>/add_rating', methods=['POST', 'GET'])
def add_rating(author_id):
        
    print(f'Это точно то {author_id} b ')
    return redirect(url_for('post.all'))
    # return render_template('comment/rating.html', author_id = author_id )
    
    # if request.method == "POST":        
                
    #     return redirect(url_for('post.all'))
    #     # try:            
    #     #     db.session.commit()            
    #     #     return redirect(url_for('post.all'))
    #     # except Exception as e:
    #     #     print(str(e))                
            
    # else:
    #     print(id) 
    #     # return render_template('main/index.html')
    #     return redirect(url_for('post.all'))